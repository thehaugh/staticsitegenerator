import unittest

from textnode import TextNode


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


if __name__ == "__main__":
    unittest.main()
