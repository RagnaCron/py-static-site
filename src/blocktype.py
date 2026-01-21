from enum import Enum

from src.parentnode import ParentNode
from src.htmlnode import HtmlNode


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []
    markdown_blocks = markdown.split("\n\n")
    for block in markdown_blocks:
        b = block.strip()
        if b != "":
            blocks.append(b)
    return blocks


def block_to_block_type(block: str) -> BlockType:
    if block.startswith("# ") or block.startswith("## ") or block.startswith("### ") or block.startswith(
            "#### ") or block.startswith("##### ") or block.startswith("###### "):
        return BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("\n```"):
        return BlockType.CODE
    elif block.startswith("> "):
        is_correct = True
        for line in block.split("\n"):
            if not line.startswith("> "):
                is_correct = False
                break
        if is_correct:
            return BlockType.QUOTE
    elif block.startswith("- "):
        is_correct = True
        for line in block.split("\n"):
            if not line.startswith("- "):
                is_correct = False
                break
        if is_correct:
            return BlockType.UNORDERED_LIST
    elif block.startswith("1. "):
        is_correct = True
        counter = 1
        for line in block.split("\n"):
            if not line.startswith(f"{counter}. "):
                is_correct = False
                break
            counter += 1
        if is_correct:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str) -> HtmlNode:
    html_node = ParentNode("div", [])

    # blocks = markdown_to_blocks(markdown)
    # for block in blocks:
    #     block_type = block_to_block_type(block)
    #     text_nodes = text_to

    return html_node

