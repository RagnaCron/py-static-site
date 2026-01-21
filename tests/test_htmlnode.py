import unittest

from src.htmlnode import HtmlNode


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HtmlNode("div", props={"class": "test"})
        self.assertEqual(node.props_to_html(), ' class="test"')

    def test_props_to_html_empty(self):
        node = HtmlNode("div")
        self.assertEqual(node.props_to_html(), "")