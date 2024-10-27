from htmlnode import HTMLNode


class LeafNode(HTMLNode):

    def __init__(self, tag=None, value=None, props=None):
        super(LeafNode, self).__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError()
        elif self.tag is None:
            return self.value
        else:
            start_tag = f"<{self.tag} {self.props_to_html()}".strip() + ">"
            return start_tag + self.value + f"</{self.tag}>"
