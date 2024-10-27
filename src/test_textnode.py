import unittest

from textnode import TextNode, text_node_to_html_node
from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq_default_url(self):
        node = TextNode("This is a text node", "bold", None)
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", "bold", "www.best.com")
        node2 = TextNode("This is a text node", "bold", "www.best.com")
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is another text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_neq_text_type(self):
        node = TextNode("This is a text node", "italic")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_neq_url(self):
        node = TextNode("This is a text node", "bold", "www.test.com")
        node2 = TextNode("This is a text node", "bold", "www.best.com")
        self.assertNotEqual(node, node2)

    def test_to_htmlnode_text(self):
        text_node = TextNode("This is a text node", "text")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(
            LeafNode(value="This is a text node").to_html(), html_node.to_html()
        )

    def test_to_htmlnode_bold(self):
        text_node = TextNode("This is a bold node", "bold")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(
            LeafNode(tag="b", value="This is a bold node").to_html(),
            html_node.to_html(),
        )

    def test_to_htmlnode_italic(self):
        text_node = TextNode("This is an italic node", "italic")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(
            LeafNode(tag="i", value="This is an italic node").to_html(),
            html_node.to_html(),
        )

    def test_to_htmlnode_code(self):
        text_node = TextNode("This is a code node", "code")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(
            LeafNode(tag="code", value="This is a code node").to_html(),
            html_node.to_html(),
        )

    def test_to_htmlnode_link(self):
        text_node = TextNode(
            "This is a link node", "link", url="https://www.boot.dev/lessons/"
        )
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(
            LeafNode(
                tag="a",
                value="This is a link node",
                props={"href": "https://www.boot.dev/lessons/"},
            ).to_html(),
            html_node.to_html(),
        )

    def test_to_htmlnode_image(self):
        text_node = TextNode("This is an image node", "image", url="/pickle.jpeg")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(
            LeafNode(
                value="",
                tag="img",
                props={"src": "/pickle.jpeg", "alt": "This is an image node"},
            ).to_html(),
            html_node.to_html(),
        )

    def test_to_htmlnode_invalid(self):
        text_node = TextNode("This is an image node", "invalid", url="/pickle.jpeg")
        with self.assertRaises(ValueError) as context_manager:
            text_node_to_html_node(text_node)
        the_exception = context_manager.exception
        self.assertEqual(type(the_exception), ValueError)
        self.assertEqual(
            str(the_exception), f"Invalid TextNode text_type: '{text_node.text_type}'"
        )


if __name__ == "__main__":
    unittest.main()
