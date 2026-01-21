import unittest

from src.blocktype import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_node


class TestBlockType(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_paragraph(self):
        block = "This is a paragraph"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
        
    def test_block_to_block_type_unordered_list(self):
        block = "- This is a list"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)
        
    def test_block_to_block_type_ordered_list(self):
        block = """1. first item
2. second item
3. third item"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)
        
    def test_block_to_block_type_code(self):
        block = "```\npython\nprint('hello world')\n```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)
        
    def test_block_to_block_type_quoted(self):
        block = "> This is a quoted text"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)
        
    def test_block_to_block_type_heading_1(self):
        block = "# This is a heading 1"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)
        
    def test_block_to_block_type_heading_2(self):
        block = "## This is heading 2"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_heading_3(self):
        block = "### This is heading 3"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_heading_4(self):
        block = "#### This is heading 4"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_heading_5(self):
        block = "##### This is heading 5"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_heading_6(self):
        block = "###### This is heading 6"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_paragraph_block(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_heading_block(self):
        md = """
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>")

    def test_code_block(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quote_block(self):
        md = """
> A nice single line quote

> A multi-line quote
> with multiple lines
> to quote
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>A nice single line quote</blockquote><blockquote>A multi-line quote\nwith multiple lines\nto quote</blockquote></div>")



if __name__ == "__main__":
    unittest.main()
