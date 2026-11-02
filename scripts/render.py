"""Deterministic, escaped static research publication. No external dependencies."""
from html import escape
from pathlib import Path
import re
import json
import shutil
from urllib.parse import urlsplit


def esc(value):
    return escape(str(value), quote=True)


def safe_url(value):
    if not isinstance(value, str) or any(ord(c) < 32 for c in value):
        return None
    parsed = urlsplit(value)
    return value if parsed.scheme in ('https', 'http') and parsed.hostname and not parsed.username and not parsed.password else None


def page(title, body, prefix=''):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · Fieldnotes Research</title><meta name="description" content="A problem-first startup research library. Evidence, uncertainty, and next questions.">
<link rel="stylesheet" href="{prefix}assets/style.css"><script src="{prefix}assets/search.js" defer></script></head>
<body><a class="skip" href="#main">Skip to content</a><header class="masthead"><a class="brand" href="{prefix}index.html"><span class="mark">F.</span> FIELDNOTES <span class="brand-sub">RESEARCH LAB</span></a><span class="edition">Independent inquiry · US focus</span></header>
<main id="main">{body}</main><footer>Fieldnotes Research Lab <span>Problems first. Evidence before confidence.</span></footer></body></html>\n'''


def value_html(value, records):
    if value is None or value == '' or value == []:
        return '<p class="unknown">Unknown / not yet investigated.</p>'
    if isinstance(value, list):
        return '<ul>' + ''.join('<li>' + value_html(v, records) + '</li>' for v in value) + '</ul>'
    if isinstance(value, dict):
        if 'text' in value and 'classification' in value:
            classification = value['classification']
            kind = 'evidence' if classification in ('observed', 'reported') else 'hypothesis'
            return f'<div class="claim {kind}"><span class="badge">{esc(classification)}</span><p>{esc(value["text"])}</p>{value_html(value.get("source_ids", []), records)}</div>'
        return '<dl>' + ''.join(f'<dt>{esc(k.replace("_", " ").capitalize())}</dt><dd>{value_html(v, records)}</dd>' for k,v in sorted(value.items())) + '</dl>'
    if isinstance(value, str) and value in records:
        return f'<a href="{esc(value)}.html">{esc(records[value]["title"])}</a> <small>({esc(value)})</small>'
    url = safe_url(value)
    if url:
        return f'<a href="{esc(url)}" rel="noopener noreferrer">{esc(value)}</a>'
    return '<p>' + esc(value) + '</p>'


def section(title, value, records, anchor):
    return f'<section id="{anchor}" class="report-section"><h2>{esc(title)}</h2>{value_html(value, records)}</section>'


def report(record, records):
    r = record
    related = [records[x] for x in r.get('related_problem_ids', []) if x in records]
    problem = r if r['type'] == 'problem' else (related[0] if related else {})
    source_ids = set(r.get('source_ids', []))
    for field in ('findings', 'evidence', 'contradictory_evidence', 'contradictory_findings'):
        for claim in r.get(field, []):
            if isinstance(claim, dict):
                source_ids.update(claim.get('source_ids', []))
    sections = [
        ('Executive summary', r.get('summary', r.get('conclusions', r.get('description', r.get('objective'))))),
        ('Customer problem', problem.get('description', r.get('objective'))),
        ('Affected customer segment', problem.get('customer_segment', r.get('potential_customers'))),
        ('Why the problem matters', problem.get('context', problem.get('problem_context'))),
        ('Supporting evidence', r.get('findings', r.get('evidence', []))),
        ('Existing solutions and competitors', r.get('alternatives', problem.get('alternatives', r.get('existing_alternatives')))),
        ('Contradictory evidence', r.get('contradictory_findings', r.get('contradictory_evidence', []))),
        ('Important uncertainties', r.get('unresolved_questions', r.get('open_questions', r.get('uncertainty')))),
        ('Potential AI-enabled opportunities', r.get('related_opportunity_ids', problem.get('related_opportunity_ids', r.get('solution_direction', [])))),
        ('Recommended next research', r.get('next_steps', r.get('next_actions', r.get('recommended_next_steps')))),
        ('Related problems', r.get('related_problem_ids', [])),
        ('Sources and references', sorted(source_ids)),
    ]
    demo = '<aside class="demo">SYNTHETIC DEMONSTRATION · Fictional content for pipeline testing. No market evidence or validated business claims.</aside>' if r.get('demo') else ''
    nav = '<nav class="contents" aria-label="Report contents"><h2>In this report</h2>' + ''.join(f'<a href="#section-{i}">{esc(title)}</a>' for i,(title,_) in enumerate(sections)) + '</nav>'
    body = demo + f'<div class="report-heading"><a class="back" href="../index.html">← Research library</a><p class="eyebrow">{esc(r["type"])} / {esc(r["id"])}</p><h1>{esc(r["title"])}</h1><p class="meta">Published {esc(r["created"])} · Revised {esc(r["updated"])} <span class="badge">{esc(r["status"])}</span></p></div>'
    body += '<div class="report-layout">' + nav + '<article>' + ''.join(section(title,val,records,f'section-{i}') for i,(title,val) in enumerate(sections))
    # Preserve all canonical entity detail, including source metadata, revenue hypotheses and decision rationale.
    body += '<section class="report-section"><h2>Record detail</h2><dl>'
    for key, val in sorted(r.items()):
        if key not in ('id','type','title','created','updated','demo','publish','history','provenance'):
            body += f'<dt>{esc(key.replace("_", " ").capitalize())}</dt><dd>{value_html(val, records)}</dd>'
    body += '</dl></section>' + section('Research provenance and revision history', {'provenance':r.get('provenance'), 'history':r.get('history')},records,'provenance') + '</article></div>'
    return page(r['title'], body, '../')


def build(records, output):
    """Render already validated records; only explicitly publishable records are emitted."""
    output = Path(output)
    selected = sorted((r for r in records if r.get('publish') is True), key=lambda r:r['id'])
    for r in selected:
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', r['id']):
            raise ValueError('Unsafe report identifier')
    mapping = {r['id']: r for r in selected}
    output.mkdir(parents=True, exist_ok=True)
    reports = output/'reports'
    reports.mkdir(exist_ok=True)
    # Remove only generated report HTML so removed/unpublished records cannot linger.
    for old in reports.glob('*.html'):
        old.unlink()
    asset_dir = output/'assets'
    asset_dir.mkdir(exist_ok=True)
    for name in ('style.css','search.js'):
        shutil.copyfile(Path(__file__).resolve().parents[1]/'assets'/name, asset_dir/name)
    for r in selected:
        (reports/(r['id']+'.html')).write_text(report(r,mapping), encoding='utf-8')
    demo = bool(selected) and all(r.get('demo') for r in selected)
    body = '<aside class="demo">SYNTHETIC DEMONSTRATION · All records below are fictional test data, excluded from the real research collection.</aside>' if demo else ''
    body += '<section class="hero"><p class="eyebrow">THE RESEARCH COLLECTION</p><h1>Better questions.<br><em>Stronger foundations.</em></h1><p class="dek">A living library of customer problems, supporting evidence, and opportunities worth investigating. Built for careful decisions, not quick convictions.</p><div class="stats"><strong>'+str(len(selected))+'</strong> published records <span>·</span> <strong>'+str(sum(r['type']=='problem' for r in selected))+'</strong> customer problems</div></section>'
    tags = sorted({tag for r in selected for tag in r.get('industries', [])})
    states = sorted({r['status'] for r in selected})
    options = lambda values: ''.join(f'<option value="{esc(v)}">{esc(v.replace("_", " "))}</option>' for v in values)
    body += '<section class="library"><div class="section-heading"><h2>Explore the library</h2><span>Most recently revised first</span></div><div class="filters"><div><label for="search">Search records</label><input id="search" type="search" placeholder="Problem, customer, or keyword…"></div><div><label for="industry">Industry</label><select id="industry"><option value="">All industries</option>'+options(tags)+'</select></div><div><label for="status">Research stage</label><select id="status"><option value="">All stages</option>'+options(states)+'</select></div></div><p id="result-count" role="status" aria-live="polite"></p><div class="cards">'
    for r in sorted(selected,key=lambda r:(r['updated'],r['id']),reverse=True):
        tags_r = r.get('industries', [])
        body += f'<article class="card" data-search="{esc(json.dumps(r, sort_keys=True, ensure_ascii=False).lower())}" data-industry="{esc("|".join(tags_r))}" data-status="{esc(r["status"])}"><div class="card-top"><span class="eyebrow">{esc(r["type"])}</span><span class="badge">{esc(r["status"])}</span></div><h3><a href="reports/{esc(r["id"])}.html">{esc(r["title"])}</a></h3><p>{esc(r.get("description", r.get("objective", "Explore the evidence, uncertainties, and next questions.")) or "Unknown / not yet investigated.")}</p><div class="card-foot"><span>{esc(" · ".join(tags_r) or "Research record")}</span><time>{esc(r["updated"])}</time></div></article>'
    body += '</div><div id="no-results" class="empty"'+(' hidden' if selected else '')+'><h3>'+('No matching records' if selected else 'The next good question starts here.')+'</h3><p>'+('Try another keyword or clear the filters.' if selected else 'No real research has been published yet. Future reviewed investigations will appear in this collection.')+'</p></div></section>'
    (output/'index.html').write_text(page('Research library',body),encoding='utf-8')
