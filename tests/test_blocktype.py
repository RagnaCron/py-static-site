import unittest

from src.blocktype import BlockType, markdown_to_blocks, block_to_block_type


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


if __name__ == "__main__":
    unittest.main()
