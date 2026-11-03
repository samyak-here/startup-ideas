"""Dependency-free record validation and deterministic publication entry point.

The schema interpreter deliberately implements only the JSON Schema keywords used
in schemas/. Unsupported keywords fail closed rather than silently doing nothing.
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urlsplit, unquote
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]


def load_records(root):
    records = []
    for path in sorted(Path(root).rglob('*.json')):
        try:
            record = json.loads(path.read_text(encoding='utf-8'))
        except (OSError, ValueError) as exc:
            raise ValueError(f'{path}: {exc}') from exc
        if not isinstance(record, dict):
            raise ValueError(f'{path}: expected one record object')
        records.append(record)
    return records


def _schema(value, schema, path):
    allowed = {'$schema','title','type','required','additionalProperties','properties','items','minItems','minLength','pattern','format','enum','const'}
    if set(schema) - allowed:
        raise ValueError(f'{path}: unsupported schema keywords {set(schema)-allowed}')
    if 'const' in schema and value != schema['const']:
        raise ValueError(f'{path}: wrong constant')
    if 'enum' in schema and value not in schema['enum']:
        raise ValueError(f'{path}: invalid value {value!r}')
    types = schema.get('type', [])
    if isinstance(types, str): types = [types]
    checks = {'null':lambda x:x is None,'string':lambda x:isinstance(x,str),'array':lambda x:isinstance(x,list),'object':lambda x:isinstance(x,dict),'boolean':lambda x:isinstance(x,bool)}
    if types and not any(checks[t](value) for t in types):
        raise ValueError(f'{path}: expected {types}')
    if isinstance(value,dict):
        missing=set(schema.get('required',[]))-set(value)
        if missing: raise ValueError(f'{path}: missing {sorted(missing)}')
        props=schema.get('properties',{})
        if schema.get('additionalProperties') is False and set(value)-set(props):
            raise ValueError(f'{path}: unknown fields {sorted(set(value)-set(props))}')
        for key,item in value.items():
            if key in props: _schema(item,props[key],f'{path}.{key}')
    if isinstance(value,list):
        if len(value)<schema.get('minItems',0): raise ValueError(f'{path}: too few items')
        for i,item in enumerate(value): _schema(item,schema.get('items',{}),f'{path}[{i}]')
    if isinstance(value,str):
        if len(value.strip())<schema.get('minLength',0): raise ValueError(f'{path}: empty text')
        if 'pattern' in schema and not re.fullmatch(schema['pattern'],value): raise ValueError(f'{path}: invalid identifier')
        if schema.get('format')=='date':
            try:
                if dt.date.fromisoformat(value).isoformat()!=value: raise ValueError()
            except ValueError: raise ValueError(f'{path}: expected YYYY-MM-DD') from None
        if schema.get('format')=='uri':
            parsed=urlsplit(value)
            if parsed.scheme not in ('http','https') or not parsed.hostname or parsed.username or parsed.password or any(ord(c)<33 for c in value):
                raise ValueError(f'{path}: unsafe source URL')


ADVANCED = ('promising', 'needs-validation', 'completed')


def _norm_url(url):
    p = urlsplit(url.strip())
    return (p.scheme.lower(), p.hostname.lower(), p.port, p.path.rstrip('/'), p.query)


def validate(records):
    by_id={}
    for record in records:
        kind=record.get('type')
        if kind not in ('problem','source','investigation','opportunity','decision'): raise ValueError('Unknown record type')
        schema=json.loads((ROOT/'schemas'/f'{kind}.schema.json').read_text())
        _schema(record,schema,record.get('id','record'))
        rid=record['id']
        if not rid.startswith(kind+'-'): raise ValueError(f'{rid}: identifier must have type prefix')
        if rid in by_id: raise ValueError(f'Duplicate identifier: {rid}')
        by_id[rid]=record
        if record['updated']<record['created']: raise ValueError(f'{rid}: updated before created')
        dates=[entry['date'] for entry in record['history']]
        if dates!=sorted(dates) or dates[0]<record['created'] or dates[-1]>record['updated']:
            raise ValueError(f'{rid}: invalid history dates')
        if record['history'][-1]['status']!=record['status']: raise ValueError(f'{rid}: status disagrees with history')
    def walk(value,owner):
        if isinstance(value,dict):
            if 'classification' in value and value['classification'] in ('observed','reported','estimate') and not value['source_ids']:
                raise ValueError(f"{owner['id']}: observed/reported/estimate claim lacks sources")
            for key,item in value.items():
                expected={'source_ids':'source','related_problem_ids':'problem','related_opportunity_ids':'opportunity'}.get(key)
                if expected:
                    if len(item)!=len(set(item)): raise ValueError(f"{owner['id']}: duplicate reference")
                    for ref in item:
                        target=by_id.get(ref)
                        if not target or target['type']!=expected: raise ValueError(f"{owner['id']}: missing or wrong-type reference {ref}")
                        if not owner['demo'] and target['demo']: raise ValueError(f"{owner['id']}: production references synthetic data")
                        if owner['publish'] and not target['publish']: raise ValueError(f"{owner['id']}: published record references private record")
                walk(item,owner)
        elif isinstance(value,list):
            for item in value: walk(item,owner)
    for record in records: walk(record,record)
    urls={}
    for record in records:
        rid=record['id']; kind=record['type']; done=record['status'] in ADVANCED
        if kind=='source':
            key=(record['demo'],_norm_url(record['url']))
            if key in urls: raise ValueError(f"{rid}: duplicate source URL already recorded as {urls[key]}")
            urls[key]=rid
            pub,acc=record['published'],record['accessed']
            if pub and pub>acc: raise ValueError(f'{rid}: published after accessed')
            if acc>record['updated']: raise ValueError(f'{rid}: accessed after record update')
        if kind=='investigation' and done and not (record['source_ids'] and record['findings']):
            raise ValueError(f'{rid}: {record["status"]} investigation needs findings and source_ids')
        if kind=='opportunity' and done and not record['related_problem_ids']:
            raise ValueError(f'{rid}: {record["status"]} opportunity must link a problem')


class _Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.ids=set(); self.lang=False; self.title=False; self.h1=False
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='html': self.lang=bool(attrs.get('lang'))
        if tag=='title': self.title=True
        if tag=='h1': self.h1=True
        if 'id' in attrs: self.ids.add(attrs['id'])
        if tag=='img' and 'alt' not in attrs: raise ValueError('Image missing alt text')
        if any(key.lower().startswith('on') for key in attrs): raise ValueError('Unsafe inline event handler')
        for key in ('href','src'):
            if key in attrs:
                if urlsplit(attrs[key]).scheme.lower() in ('javascript','data','vbscript'): raise ValueError('Unsafe link')
                self.links.append(attrs[key])


def check_site(output):
    root=Path(output).resolve(); pages={}
    if not (root/'index.html').is_file(): raise ValueError('Missing library homepage')
    for path in root.rglob('*.html'):
        page=_Page(); page.feed(path.read_text(encoding='utf-8'))
        if not (page.lang and page.title and page.h1): raise ValueError(f'{path}: missing language/title/h1')
        pages[path.resolve()]=page
    for path,page in pages.items():
        for link in page.links:
            parsed=urlsplit(link)
            if parsed.scheme or parsed.netloc: continue
            target=(path.parent/unquote(parsed.path)).resolve() if parsed.path else path
            if not target.is_relative_to(root): raise ValueError(f'{path}: link escapes output: {link}')
            if target.is_dir(): target=target/'index.html'
            if not target.exists(): raise ValueError(f'{path}: broken link {link}')
            if parsed.fragment and target in pages and unquote(parsed.fragment) not in pages[target].ids:
                raise ValueError(f'{path}: missing anchor {link}')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['validate','build','check'])
    parser.add_argument('--demo',action='store_true')
    parser.add_argument('--output',default='site')
    args=parser.parse_args()
    records=load_records(ROOT/'knowledge')
    if any(r.get('demo') for r in records): raise ValueError('Demo records must live in examples/')
    demo=load_records(ROOT/'examples') if args.demo else []
    validate(records+demo)
    if demo and any(not r['demo'] for r in demo): raise ValueError('Examples must be marked synthetic')
    if args.command!='validate':
        from render import build
        output=Path(args.output)
        demo_output=output/'demo'
        marker=demo_output/'.lab-generated'
        if demo_output.exists() and not args.demo:
            if not marker.is_file():
                raise ValueError('Refusing to remove unmarked demo output; choose a fresh --output directory')
            shutil.rmtree(demo_output)
        build([r for r in records if r['publish']],output)
        if args.demo:
            build([r for r in demo if r['publish']],demo_output)
            marker.write_text('Generated synthetic demonstration output. Safe to rebuild.\n')
            homepage=output/'index.html'
            homepage.write_text(homepage.read_text().replace('</main>', '<aside class="demo"><a href="demo/index.html">Explore the synthetic demonstration</a> — fictional pipeline examples, excluded from real research.</aside></main>'))
            demo_index=demo_output/'index.html'
            demo_index.write_text(demo_index.read_text().replace('</main>', '<p><a href="../index.html">Return to the real research library</a></p></main>'))
        check_site(output)
    print(f'{args.command}: validated {len(records)} research and {len(demo)} synthetic records')


if __name__=='__main__':
    try: main()
    except (ValueError,OSError) as exc: raise SystemExit(f'ERROR: {exc}') from exc
