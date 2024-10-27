from htmlnode import HTMLNode
from functools import reduce


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super(ParentNode, self).__init__(
            tag=tag, value=None, children=children, props=props
        )

    def to_html(self):
        if self.tag is None:
            raise ValueError("A ParentNode must have a tag.")
        elif self.children is None or len(self.children) == 0:
            raise ValueError("A ParentNode must have children.")
        else:
            start_tag = f"<{self.tag} {self.props_to_html()}".strip() + ">"
            nested_html = reduce(lambda x, y: x + y.to_html(), self.children, "")
            return start_tag + nested_html + f"</{self.tag}>"
