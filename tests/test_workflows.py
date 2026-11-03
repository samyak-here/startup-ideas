"""Guard the publication boundary in the Pages workflow.

Regression test for audit finding P0-1 (2026-11-02): the workflow built the
synthetic demo into the same site/ directory it uploaded, so fictional
records were deployed to the production library.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PagesWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.pages = (ROOT / '.github' / 'workflows' / 'pages.yml').read_text()

    def test_demo_validation_does_not_target_the_uploaded_directory(self):
        bare = re.findall(r'-\s+run:\s+python3 scripts/lab\.py check --demo\s*$', self.pages, re.M)
        self.assertEqual(bare, [], 'check --demo without --output builds the demo into site/')
        self.assertIn('check --demo --output', self.pages)

    def test_uploaded_site_is_a_production_only_build(self):
        self.assertIn('python3 scripts/lab.py check --output site', self.pages)
        self.assertIn('test ! -e site/demo', self.pages)
        self.assertIn('path: site', self.pages)

    def test_deploy_stays_on_default_branch_with_least_privilege(self):
        self.assertIn("branches: [main]", self.pages)
        self.assertIn('contents: read', self.pages)


if __name__ == '__main__':
    unittest.main()
