"""Behavioral regression tests for record integrity and publication safety."""
import copy
import json
from pathlib import Path
import sys
import subprocess
import shutil
import tempfile
import unittest
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import lab
import render


def fixtures():
    return [json.loads(p.read_text()) for p in sorted((ROOT / 'examples').glob('*.json'))]


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.links = []
        self.ids = set()
        self.labels = set()
        self.controls = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        if tag == 'label' and 'for' in attrs:
            self.labels.add(attrs['for'])
        if tag in ('input', 'select', 'textarea'):
            self.controls.append(attrs)
        for key in ('href', 'src'):
            if key in attrs:
                self.links.append(attrs[key])


class IntegrityTests(unittest.TestCase):
    def setUp(self):
        self.records = fixtures()
        self.problem = next(r for r in self.records if r['type'] == 'problem')
        self.source = next(r for r in self.records if r['type'] == 'source')

    def test_empty_library_is_valid(self):
        lab.validate([])

    def test_complete_related_fixture_is_valid(self):
        self.assertEqual(len(self.records), 5)
        lab.validate(self.records)

    def test_missing_required_metadata(self):
        del self.problem['customer_segment']
        with self.assertRaises(ValueError):
            lab.validate(self.records)

    def test_wrong_field_type(self):
        self.problem['industries'] = 'not a list'
        with self.assertRaises(ValueError):
            lab.validate(self.records)

    def test_duplicate_ids(self):
        self.records.append(copy.deepcopy(self.problem))
        with self.assertRaises(ValueError):
            lab.validate(self.records)

    def test_missing_source(self):
        self.records.remove(self.source)
        with self.assertRaises(ValueError):
            lab.validate(self.records)

    def test_missing_related_record(self):
        self.problem['related_problem_ids'] = ['problem-missing']
        with self.assertRaises(ValueError):
            lab.validate(self.records)

    def test_public_record_cannot_reference_private_source(self):
        self.source['publish'] = False
        with self.assertRaises(ValueError):
            lab.validate(self.records)

    def test_real_record_cannot_reference_demo(self):
        self.problem['demo'] = False
        with self.assertRaises(ValueError):
            lab.validate(self.records)

    def test_wrong_reference_type(self):
        self.problem['related_problem_ids'] = [self.source['id']]
        with self.assertRaises(ValueError):
            lab.validate(self.records)

    def test_invalid_lifecycle(self):
        self.problem['status'] = 'commercially-proven'
        with self.assertRaises(ValueError):
            lab.validate(self.records)

    def test_status_history_must_match(self):
        self.problem['status'] = 'archived'
        with self.assertRaises(ValueError):
            lab.validate(self.records)

    def test_impossible_date(self):
        self.problem['created'] = '2026-02-31'
        with self.assertRaises(ValueError):
            lab.validate(self.records)

    def test_observed_claim_requires_citation(self):
        self.problem['evidence'] = [{'text': 'A factual assertion', 'classification': 'observed', 'source_ids': []}]
        with self.assertRaises(ValueError):
            lab.validate(self.records)

    def test_unsafe_source_url(self):
        for url in ('javascript:alert(1)', 'data:text/html,<script>alert(1)</script>'):
            with self.subTest(url=url):
                self.source['url'] = url
                with self.assertRaises(ValueError):
                    lab.validate(self.records)

    def test_identifier_cannot_escape_output_directory(self):
        self.problem['id'] = '../../outside'
        with self.assertRaises(ValueError):
            lab.validate(self.records)


class AuditRegressionTests(unittest.TestCase):
    """Regression tests for the 2026-11-02 independent audit findings."""

    def setUp(self):
        self.records = fixtures()
        self.problem = next(r for r in self.records if r['type'] == 'problem')
        self.source = next(r for r in self.records if r['type'] == 'source')

    def _rename_problem(self, new_id):
        old = self.problem['id']
        def swap(value):
            if isinstance(value, list):
                return [new_id if item == old else item for item in value]
            if isinstance(value, dict):
                return {k: swap(v) for k, v in value.items()}
            return value
        for record in self.records:
            for key in list(record):
                record[key] = swap(record[key])
        self.problem['id'] = new_id

    def test_placeholder_title_is_rejected(self):
        self.problem['title'] = 'Replace with descriptive title'
        with self.assertRaises(ValueError):
            lab.validate(self.records)

    def test_short_sequential_id_is_rejected_for_real_records(self):
        self._rename_problem('problem-1')
        self.problem['demo'] = False
        # Isolate the ID rule: a production record may not reference demo data,
        # so validate this record alone (it has no references of its own that
        # point at demo records except opportunities — clear them).
        self.problem['related_opportunity_ids'] = []
        with self.assertRaises(ValueError):
            lab.validate([self.problem])

    def test_trailing_hyphen_id_is_rejected(self):
        self._rename_problem('problem-demo-')
        with self.assertRaises(ValueError):
            lab.validate(self.records)

    def test_self_reference_is_rejected(self):
        self.problem['related_problem_ids'] = [self.problem['id']]
        with self.assertRaises(ValueError):
            lab.validate(self.records)

    def test_duplicate_source_url_is_rejected(self):
        clone = copy.deepcopy(self.source)
        clone['id'] = 'source-87654321'
        self.records.append(clone)
        with self.assertRaises(ValueError):
            lab.validate(self.records)

    def test_completed_investigation_requires_sourced_findings(self):
        inv = next(r for r in self.records if r['type'] == 'investigation')
        inv['findings'] = []
        inv['source_ids'] = []
        inv['status'] = 'completed'
        inv['history'][-1]['status'] = 'completed'
        with self.assertRaises(ValueError):
            lab.validate(self.records)

    def test_source_accessed_before_publication_is_rejected(self):
        self.source['published'] = '2025-06-06'
        self.source['accessed'] = '2020-01-01'
        with self.assertRaises(ValueError):
            lab.validate(self.records)

    def test_credential_shaped_text_is_rejected(self):
        self.problem['description'] = 'leaked key sk-' + 'A' * 24
        with self.assertRaises(ValueError):
            lab.validate(self.records)

    def test_knowledge_loader_enforces_type_directory_and_filename(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            bad_root = base / 'bad'
            (bad_root / 'wrongdir').mkdir(parents=True)
            (bad_root / 'wrongdir' / 'random.json').write_text(json.dumps(self.problem))
            with self.assertRaises(ValueError):
                lab.load_knowledge(bad_root)
            good_root = base / 'good'
            (good_root / 'problems').mkdir(parents=True)
            (good_root / 'problems' / (self.problem['id'] + '.json')).write_text(json.dumps(self.problem))
            self.assertEqual([r['id'] for r in lab.load_knowledge(good_root)], [self.problem['id']])


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.out = Path(self.temp.name) / 'site'
        self.records = fixtures()

    def pages(self):
        return {p.relative_to(self.out).as_posix(): p.read_bytes() for p in self.out.rglob('*') if p.is_file()}

    def test_empty_library_has_useful_page(self):
        render.build([], self.out)
        text = (self.out / 'index.html').read_text()
        self.assertIn('<html', text)
        self.assertRegex(text.lower(), r'no (published |real |research )?(reports|research|records|findings)|empty|awaiting|first')

    def test_deterministic_build_and_stable_paths(self):
        render.build(self.records, self.out)
        first = self.pages()
        render.build(list(reversed(self.records)), self.out)
        self.assertEqual(first, self.pages())
        for record in self.records:
            self.assertTrue((self.out / 'reports' / (record['id'] + '.html')).is_file(), record['id'])

    def test_html_escaping(self):
        payload = '<img src=x onerror="alert(1)">'
        self.records[0]['title'] = payload
        render.build(self.records, self.out)
        text = (self.out / 'reports' / (self.records[0]['id'] + '.html')).read_text()
        self.assertIn('&lt;img', text)
        self.assertNotIn(payload, text)
        for tag, attrs in Page(text).tags:
            self.assertFalse(any(k.startswith('on') for k in attrs), (tag, attrs))

    def test_navigation_and_accessibility(self):
        render.build(self.records, self.out)
        pages = {p: Page(p.read_text()) for p in self.out.rglob('*.html')}
        self.assertGreater(len(pages), 1)
        for path, page in pages.items():
            with self.subTest(page=path.name):
                self.assertTrue(any(tag == 'html' and attrs.get('lang') for tag, attrs in page.tags))
                self.assertTrue(any(tag == 'title' for tag, _ in page.tags))
                self.assertTrue(any(tag == 'main' for tag, _ in page.tags))
                self.assertTrue(any(tag == 'h1' for tag, _ in page.tags))
                for control in page.controls:
                    self.assertTrue(control.get('aria-label') or control.get('aria-labelledby') or control.get('id') in page.labels)
                for href in page.links:
                    url = urlsplit(href)
                    if url.scheme or url.netloc:
                        self.assertIn(url.scheme, ('https', 'http'))
                        continue
                    self.assertFalse(url.path.startswith('/'), 'Must work under a repository subpath')
                    target = (path.parent / unquote(url.path)).resolve() if url.path else path
                    self.assertTrue(target.exists(), (path.name, href))
                    if url.fragment and target in pages:
                        self.assertIn(unquote(url.fragment), pages[target].ids)

    def test_private_records_are_excluded_and_stale_pages_removed(self):
        render.build(self.records, self.out)
        hidden = self.records[0]
        old_page = self.out / 'reports' / (hidden['id'] + '.html')
        self.assertTrue(old_page.exists())
        hidden['publish'] = False
        hidden['title'] = 'PRIVATE NEVER PUBLISH'
        render.build(self.records, self.out)
        self.assertFalse(old_page.exists())
        for data in self.pages().values():
            self.assertNotIn(b'PRIVATE NEVER PUBLISH', data)
        render.build([], self.out)
        self.assertEqual(list((self.out / 'reports').glob('*.html')), [])

    def test_renderer_does_not_link_unsafe_urls(self):
        source = next(r for r in self.records if r['type'] == 'source')
        source['url'] = 'javascript:alert(1)'
        render.build(self.records, self.out)
        page = Page((self.out / 'reports' / (source['id'] + '.html')).read_text())
        self.assertFalse(any(link.startswith('javascript:') for link in page.links))

    def test_check_site_rejects_missing_page(self):
        render.build(self.records, self.out)
        lab.check_site(self.out)
        (self.out / 'reports' / (self.records[0]['id'] + '.html')).unlink()
        with self.assertRaises(ValueError):
            lab.check_site(self.out)

    def test_cli_keeps_demo_separate(self):
        isolated = Path(self.temp.name) / 'repository'
        isolated.mkdir()
        for directory in ('scripts', 'schemas', 'examples', 'assets'):
            shutil.copytree(ROOT / directory, isolated / directory)
        (isolated / 'knowledge').mkdir()
        result = subprocess.run([sys.executable, str(isolated / 'scripts/lab.py'), 'check', '--demo', '--output', str(self.out)], cwd=isolated, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.out / 'demo/index.html').exists())
        self.assertEqual(list((self.out / 'reports').glob('*.html')), [])
        for record in self.records:
            self.assertNotIn(record['title'], (self.out / 'index.html').read_text())
            self.assertTrue((self.out / 'demo/reports' / (record['id'] + '.html')).exists())
        result = subprocess.run([sys.executable, str(isolated / 'scripts/lab.py'), 'check', '--output', str(self.out)], cwd=isolated, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.out / 'demo').exists(), 'Ordinary publication must remove retained demo outputs')

    def test_synthetic_content_is_labeled(self):
        render.build(self.records, self.out)
        for path in self.out.rglob('*.html'):
            self.assertRegex(path.read_text().lower(), r'demonstration|synthetic')

    def test_empty_narrative_sections_are_omitted_from_reports(self):
        render.build(self.records, self.out)
        source = next(r for r in self.records if r['type'] == 'source')
        text = (self.out / 'reports' / (source['id'] + '.html')).read_text()
        self.assertNotIn('Customer problem', text)
        self.assertIn('Record detail', text)

    def test_library_has_record_type_filter_and_curated_search_index(self):
        render.build(self.records, self.out)
        text = (self.out / 'index.html').read_text()
        self.assertIn('id="kind"', text)
        self.assertIn('data-kind="problem"', text)
        self.assertNotIn('data-search', text)
        index = json.loads((self.out / 'search-index.json').read_text())
        joined = ' '.join(row['text'] for row in index)
        for noise in ('source_ids', 'provenance', 'bootstrap-demo'):
            self.assertNotIn(noise, joined)


class SecondAuditRegressionTests(unittest.TestCase):
    """Rules added by the 2026-11-03 independent audit (see docs/audits/)."""
    def prod(self):
        # Production IDs need collision-resistant suffixes, so rename the short synthetic IDs consistently.
        text = json.dumps(fixtures())
        for kind in ('problem', 'source', 'investigation', 'opportunity', 'decision'):
            text = text.replace(f'{kind}-demo', f'{kind}-0a1b2c3d4e5f')
        recs = json.loads(text)
        for r in recs:
            r['demo'] = False
            r['title'] = r['title'].replace('DEMONSTRATION \u2014 ', '')
            r['provenance'] = {'agent': 'test-agent', 'session': 'test-session'}
        return recs

    def kind(self, recs, k):
        return next(r for r in recs if r['type'] == k)

    def rejects(self, recs, text):
        with self.assertRaisesRegex(ValueError, text):
            lab.validate(recs)

    def test_baseline_production_copy_is_valid(self):
        lab.validate(self.prod())

    def test_completed_investigation_needs_sources_and_findings(self):
        recs = self.prod(); i = self.kind(recs, 'investigation')
        i.update(status='completed', source_ids=[], findings=[])
        i['history'][-1]['status'] = 'completed'
        self.rejects(recs, 'needs findings')

    def test_promising_opportunity_needs_problem(self):
        recs = self.prod(); o = self.kind(recs, 'opportunity')
        o.update(status='promising', related_problem_ids=[])
        o['history'][-1]['status'] = 'promising'
        self.rejects(recs, 'must link a problem')

    def test_duplicate_source_url_rejected(self):
        recs = self.prod(); dup = copy.deepcopy(self.kind(recs, 'source'))
        dup['id'] = 'source-dup0a1b2c3d4e5f'; dup['url'] = dup['url'].upper().replace('HTTPS', 'https') + '/'
        recs.append(dup)
        self.rejects(recs, 'duplicate source URL')

    def test_source_dates_must_be_ordered(self):
        recs = self.prod(); self.kind(recs, 'source')['published'] = '2099-01-01'
        self.rejects(recs, 'accessed before its publication')

    def test_unsourced_estimate_rejected(self):
        recs = self.prod(); p = self.kind(recs, 'problem')
        p['evidence'] = [{'text': 'Market is $50B', 'classification': 'estimate', 'source_ids': []}]
        self.rejects(recs, 'lacks sources')

    def test_search_text_is_external_and_type_filter_present(self):
        out = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, out, True)
        render.build(fixtures(), out)
        home = (out / 'index.html').read_text()
        self.assertIn('id="kind"', home)
        self.assertNotIn('data-search', home)
        index = json.loads((out / 'search-index.json').read_text())
        self.assertEqual(len(index), 5)

    def test_private_records_not_in_search_index(self):
        recs = fixtures(); recs[0]['publish'] = False
        out = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, out, True)
        render.build(recs, out)
        ids = {row['id'] for row in json.loads((out / 'search-index.json').read_text())}
        self.assertNotIn(recs[0]['id'], ids)


if __name__ == '__main__':
    unittest.main()
