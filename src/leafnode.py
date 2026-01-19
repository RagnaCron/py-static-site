from htmlnode import HtmlNode


class LeafNode(HtmlNode):
    def __init__(self, tag: str, value: str, props: dict = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("value cannot be empty")
        if self.tag is None or self.tag == "":
            return self.value
        else:
            if self.tag == "img":
                return f"<{self.tag}{self.props_to_html()}/>"
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"