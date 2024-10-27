from leafnode import LeafNode

TEXT_TYPE_TEXT = "text"
TEXT_TYPE_BOLD = "bold"
TEXT_TYPE_ITALIC = "italic"
TEXT_TYPE_CODE = "code"
TEXT_TYPE_LINK = "link"
TEXT_TYPE_IMAGE = "image"


class TextNode:

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __str__(self):
        return f"{type(self).__name__}({self.text}, {self.text_type}, {self.url})"

    def __repr__(self):
        return self.__str__()


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match (text_node.text_type):
        case "text":
            return LeafNode(value=text_node.text)
        case "bold":
            return LeafNode(tag="b", value=text_node.text)
        case "italic":
            return LeafNode(tag="i", value=text_node.text)
        case "code":
            return LeafNode(tag="code", value=text_node.text)
        case "link":
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case "image":
            return LeafNode(
                value="",
                tag="img",
                props={"src": text_node.url, "alt": text_node.text},
            )
        case _:
            raise ValueError(f"Invalid TextNode text_type: '{text_node.text_type}'")


if __name__ == "__main__":
    a = TextNode("test", "bold", "www.test.com")
    print(a)
