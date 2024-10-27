import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_tohtml_no_value(self):
        leaf_node = LeafNode()
        self.assertRaises(ValueError, leaf_node.to_html)

    def test_tohtml_value_only(self):
        leaf_node = LeafNode(value="a test paragraph")
        self.assertEqual("a test paragraph", leaf_node.to_html())

    def test_tohtml_tag_only(self):
        leaf_node = LeafNode("p", "a test paragraph")
        self.assertEqual("<p>a test paragraph</p>", leaf_node.to_html())

    def test_tohtml_properties(self):
        leaf_node = LeafNode("p", "a test paragraph", {"id": "name", "class": "test"})
        self.assertEqual(
            '<p id="name" class="test">a test paragraph</p>', leaf_node.to_html()
        )
