"""Keep provider-neutral onboarding navigable as documentation evolves."""
import re
import unittest
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]

class DocumentationTests(unittest.TestCase):
    def test_local_markdown_links_exist(self):
        # Every Markdown file is onboarding surface for some agent — not just
        # root and docs/. operations/, templates/, .github/, knowledge/ and
        # schemas/ links rotted silently before this scan covered them.
        files = [p for p in ROOT.rglob('*.md') if '.git' not in p.parts]
        for path in files:
            for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)', path.read_text()):
                parsed = urlsplit(link)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                target = path.parent / unquote(parsed.path)
                with self.subTest(file=str(path.relative_to(ROOT)), link=link):
                    self.assertTrue(target.exists(), f'Missing documentation target: {target}')
