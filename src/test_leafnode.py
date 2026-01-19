import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("div", "Hello")
        self.assertEqual(node.to_html(), "<div>Hello</div>")

    def test_to_html_empty_value(self):
        node = LeafNode("p", "")
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello")
        self.assertEqual(node.to_html(), "Hello")

    def test_to_html_props(self):
        node = LeafNode("div", "Hello", props={"class": "test"})
        self.assertEqual(node.to_html(), '<div class="test">Hello</div>')

