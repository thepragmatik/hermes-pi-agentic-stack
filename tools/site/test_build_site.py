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


if __name__ == "__main__":
    unittest.main(verbosity=2)
