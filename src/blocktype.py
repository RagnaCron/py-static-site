from enum import Enum
from typing import Any

from src.leafnode import LeafNode
from src.parentnode import ParentNode
from src.textnode import text_node_to_html_node, TextNode, TextType, text_to_textnodes


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


def paragraph_node(block) -> list[LeafNode]:
    html_nodes = []
    block = block.replace("\n", " ")
    text_blocks = text_to_textnodes(block)
    for text_block in text_blocks:
        html_nodes.append(text_node_to_html_node(text_block))
    return html_nodes


def heading_node(block) -> LeafNode:
    heading_level = block.count("#")
    return LeafNode(f"h{heading_level}", block[heading_level:].strip())


def quote_node(block) -> list[LeafNode]:
    html_nodes = []
    block = block.replace("> ", "").replace("\n", " ")
    text_blocks = text_to_textnodes(block)
    for text_block in text_blocks:
        if text_block.text == "":
            continue
        html_nodes.append(text_node_to_html_node(text_block))
    return html_nodes


def unordered_list_node(block) -> list[ParentNode]:
    html_nodes = []
    block = block.replace("- ", "")
    blocks = block.split("\n")
    return create_list_node(blocks, html_nodes)


def ordered_list_node(block) -> list[ParentNode]:
    html_nodes = []
    counter = 1
    blocks = []
    for block in block.split("\n"):
        blocks.append(block.replace(f"{counter}. ", ""))
        counter += 1
    return create_list_node(blocks, html_nodes)


def create_list_node(blocks: list[Any], html_nodes: list[Any]) -> list[Any]:
    text_blocks = []
    for block in blocks:
        text_blocks.append(text_to_textnodes(block))
    for text_block in text_blocks:
        nodes = []
        for n in text_block:
            nodes.append(text_node_to_html_node(n))
        html_nodes.append(ParentNode("li", nodes))
    return html_nodes


def markdown_to_html_node(markdown: str) -> ParentNode:
    html_node = ParentNode("div", [])

    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                html_node.children.append(ParentNode("p", paragraph_node(block)))
            case BlockType.HEADING:
                html_node.children.append(heading_node(block))
            case BlockType.CODE:
                block = block.replace("```\n", "").replace("```", "")
                html_node.children.append(ParentNode("pre", [text_node_to_html_node(TextNode(block, TextType.CODE))]))
            case BlockType.QUOTE:
                html_node.children.append(ParentNode("blockquote", quote_node(block)))
            case BlockType.UNORDERED_LIST:
                html_node.children.append(ParentNode("ul", unordered_list_node(block)))
            case BlockType.ORDERED_LIST:
                html_node.children.append(ParentNode("ol", ordered_list_node(block)))

    return html_node
