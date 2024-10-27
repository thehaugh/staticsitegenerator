from unittest import TestCase

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(TestCase):
    def test_tohtml_only_leafs(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
            node.to_html(),
        )

    def test_tohtml_nested_parents(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                ParentNode("p", [LeafNode("b", "A sneaky nested parent... bold")]),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            (
                "<p><b>Bold text</b><p><b>A sneaky nested parent... bold</b></p>"
                "<i>italic text</i>Normal text</p>"
            ),
            node.to_html(),
        )

    def test_tohtml_nested_parents_with_props(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                ParentNode(
                    "p",
                    [
                        LeafNode(
                            "b", "A sneaky nested parent... bold", props={"id": "test"}
                        ),
                        ParentNode(
                            "p",
                            [LeafNode("i", "italic text")],
                            props={"id": "parent id"},
                        ),
                    ],
                ),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            (
                '<p><b>Bold text</b><p><b id="test">A sneaky nested parent... bold</b>'
                '<p id="parent id"><i>italic text</i></p></p>'
                "<i>italic text</i>Normal text</p>"
            ),
            node.to_html(),
        )

    def test_tohtml_no_tag(self):
        node = ParentNode(
            children=[
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        with self.assertRaises(ValueError) as context_manager:
            node.to_html()
        the_exception = context_manager.exception
        self.assertEqual(type(the_exception), ValueError)
        self.assertEqual(str(the_exception), "A ParentNode must have a tag.")

    def test_tohtml_no_children(self):
        node = ParentNode(tag="p")
        with self.assertRaises(ValueError) as context_manager:
            node.to_html()
        the_exception = context_manager.exception
        self.assertEqual(type(the_exception), ValueError)
        self.assertEqual(str(the_exception), "A ParentNode must have children.")
