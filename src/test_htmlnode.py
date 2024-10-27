import unittest

from htmlnode import HTMLNode


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        html_node = HTMLNode(
            tag="p",
            value="test",
            props={"href": "https://www.google.com", "target": "_blank"},
        )
        html_props = html_node.props_to_html()
        self.assertEqual('href="https://www.google.com" target="_blank"', html_props)

    def test_props_to_html_empty(self):
        html_node = HTMLNode(tag="p", value="test")
        html_props = html_node.props_to_html()
        self.assertEqual("", html_props)

    def test_html_node_repr(self):
        html_node_child = HTMLNode(tag="p", value="test")
        html_node = HTMLNode(
            tag="p",
            value="test",
            children=[html_node_child],
            props={"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(
            (
                "HTMLNode(p, test, [HTMLNode(p, test, None, None)], "
                "{'href': 'https://www.google.com', 'target': '_blank'})"
            ),
            str(html_node),
        )


if __name__ == "__main__":
    unittest.main()
