import unittest

from leafnode import LeafNode
from parentnode import ParentNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_parent_parent(self):
        parent_node = ParentNode("grandparent", [
            ParentNode("parent", [
                LeafNode("b", "grandchild")
            ])
        ])
        self.assertEqual(parent_node.to_html(), "<grandparent><parent><b>grandchild</b></parent></grandparent>")