#!/usr/bin/env python3
"""Unit tests for build_site.py render_md table + diagram features."""
from pathlib import Path
import sys, unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_site as bs


class TableTests(unittest.TestCase):
    def test_pipe_table_becomes_real_table(self):
        md = "| A | B |\n|---|---|\n| one | two |\n"
        html_out = bs.render_md(md, "index.html")
        self.assertIn("<table", html_out)
        self.assertIn("<th>A</th>", html_out)
        self.assertIn("<td>one</td>", html_out)
        self.assertNotIn('<pre class="md-table">', html_out)

    def test_table_escapes_html(self):
        md = "| A |\n|---|\n| `<b>` |\n"
        html_out = bs.render_md(md, "index.html")
        self.assertIn("&lt;b&gt;", html_out)

    def test_bold_inside_cell(self):
        md = "| A |\n|---|\n| **initial router** |\n"
        html_out = bs.render_md(md, "index.html")
        self.assertIn("<strong>initial router</strong>", html_out)


class DiagramTests(unittest.TestCase):
    def test_diagram_map_exists(self):
        self.assertTrue(hasattr(bs, "DIAGRAMS"))
        self.assertIn("research/routing.html", bs.DIAGRAMS)


class ValidatorTests(unittest.TestCase):
    def test_validator_checks_svgs_and_tables(self):
        src = (bs.ROOT / "tools/site/validate_site.py").read_text()
        self.assertIn('glob("*.svg")', src)
        self.assertIn("raw table dump present", src)


class DarkModeCssTests(unittest.TestCase):
    def test_tables_styled_in_dark_mode(self):
        css = bs.layout("t", "x", "p", "r.md")
        dark = css.split("prefers-color-scheme:dark")[1]
        self.assertIn("th{", dark)
        self.assertIn("td{", dark)
        self.assertIn("tbody tr:nth-child(even)", dark)


class OrderedTests(unittest.TestCase):
    def test_ordered_list_becomes_ol(self):
        md = "1. one\n2. two\n"
        html_out = bs.render_md(md, "index.html")
        self.assertIn("<ol>", html_out)
        self.assertIn("<li>two</li>", html_out)


if __name__ == "__main__":
    unittest.main(verbosity=2)


if __name__ == "__main__":
    unittest.main(verbosity=2)


