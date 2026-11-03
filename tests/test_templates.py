"""Templates are contribution starting points: they must stay structurally
valid against their schemas, and must never pass full validation as records.
"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import lab

TYPES = ('problem', 'source', 'investigation', 'opportunity', 'decision')


class TemplateTests(unittest.TestCase):
    def templates(self):
        return {p.stem: json.loads(p.read_text()) for p in sorted((ROOT / 'templates').glob('*.json'))}

    def test_every_record_type_has_a_template(self):
        self.assertEqual(sorted(self.templates()), sorted(TYPES))

    def test_templates_match_their_schemas(self):
        for kind, template in self.templates().items():
            with self.subTest(template=kind):
                schema = json.loads((ROOT / 'schemas' / f'{kind}.schema.json').read_text())
                lab._schema(template, schema, template['id'])

    def test_templates_are_rejected_as_real_records(self):
        for kind, template in self.templates().items():
            with self.subTest(template=kind):
                with self.assertRaises(ValueError):
                    lab.validate([template])


if __name__ == '__main__':
    unittest.main()
