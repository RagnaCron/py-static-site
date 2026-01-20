import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, \
    extract_markdown_links


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.google.com")
        node2 = TextNode("This is a link node", TextType.LINK, "https://www.google.com")
        self.assertEqual(node, node2)

    def test_not_eq_diff_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_diff_types(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node3)

    def test_not_eq_none_url(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.google.com")
        node2 = TextNode("This is a link node", TextType.LINK, None)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props["href"], "https://www.google.com")
        self.assertEqual(html_node.to_html(), "<a href=\"https://www.google.com\">This is a link node</a>")

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://www.google.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "https://www.google.com/image.png")
        self.assertEqual(html_node.props["alt"], "This is an image node")
        self.assertEqual(html_node.to_html(), "<img src=\"https://www.google.com/image.png\" alt=\"This is an image node\"/>")

    def test_delimiter_code(self):
        node = TextNode("This is text with a `code block` word.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[2].text, " word.")

    def test_delimiter_bold(self):
        node = TextNode("This is text with a **bold** word.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[2].text, " word.")

    def test_delimiter_italic(self):
        node = TextNode("This is text with a _italic_ word.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[2].text, " word.")

    def test_delimiter_missing(self):
        node = TextNode("This is text with a missing `delimiter.", TextType.TEXT)
        self.assertRaises(ValueError, lambda: split_nodes_delimiter([node], "`", TextType.CODE))

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with an [image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

if __name__ == "__main__":
    unittest.main()
