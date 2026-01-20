import re
from typing import List, Tuple
from enum import Enum

from leafnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Unsupported text type: {text_node.text_type}")


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts, indices = split_by_delimiter_with_indexes(node.text, delimiter)
        for i in range(len(parts)):
            if i in indices:
                new_nodes.append(TextNode(parts[i], text_type))
            else:
                new_nodes.append(TextNode(parts[i], TextType.TEXT))

    return new_nodes

def split_by_delimiter_with_indexes(text: str, delimiter: str) -> Tuple[List[str], List[int]]:
    d = re.escape(delimiter)
    pattern = re.compile(rf"{d}(.*?){d}")

    parts: List[str] = []
    delimited_indexes: List[int] = []

    matches = list(pattern.finditer(text))
    if text.count(delimiter) != len(matches) * 2:
        raise ValueError(f"Unclosed delimiter: {delimiter}")

    last_end = 0
    for match in pattern.finditer(text):
        parts.append(text[last_end:match.start()])
        parts.append(match.group(1))
        delimited_indexes.append(len(parts) - 1)
        last_end = match.end()

    parts.append(text[last_end:])

    return parts, delimited_indexes
