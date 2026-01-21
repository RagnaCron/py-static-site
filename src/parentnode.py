from src.htmlnode import HtmlNode


class ParentNode(HtmlNode):
    def __init__(self, tag: str, children: list, props: dict = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None or self.tag == "":
            raise ValueError("tag cannot be empty")
        if self.children is None or len(self.children) == 0:
            raise ValueError("children cannot be empty")

        html = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"
        return html

    def __repr__(self):
        return f"ParentNode(tag='{self.tag}', children={self.children}, props={self.props})"

