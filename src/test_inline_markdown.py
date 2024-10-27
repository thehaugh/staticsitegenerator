from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_link,
    split_nodes_image,
    text_to_textnodes,
)
from textnode import (
    TextNode,
    TEXT_TYPE_TEXT,
    TEXT_TYPE_BOLD,
    TEXT_TYPE_ITALIC,
    TEXT_TYPE_CODE,
    TEXT_TYPE_LINK,
    TEXT_TYPE_IMAGE,
)
from unittest import TestCase


class TestInlineMarkdown(TestCase):

    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TEXT_TYPE_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TEXT_TYPE_CODE)
        expected_nodes = [
            TextNode("This is text with a ", TEXT_TYPE_TEXT),
            TextNode("code block", TEXT_TYPE_CODE),
            TextNode(" word", TEXT_TYPE_TEXT),
        ]
        self.assertListEqual(expected_nodes, new_nodes)

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is text with a **bold** word", TEXT_TYPE_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TEXT_TYPE_BOLD)
        expected_nodes = [
            TextNode("This is text with a ", TEXT_TYPE_TEXT),
            TextNode("bold", TEXT_TYPE_BOLD),
            TextNode(" word", TEXT_TYPE_TEXT),
        ]
        self.assertListEqual(expected_nodes, new_nodes)

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is text with a *italic* word", TEXT_TYPE_TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TEXT_TYPE_ITALIC)
        expected_nodes = [
            TextNode("This is text with a ", TEXT_TYPE_TEXT),
            TextNode("italic", TEXT_TYPE_ITALIC),
            TextNode(" word", TEXT_TYPE_TEXT),
        ]
        self.assertListEqual(expected_nodes, new_nodes)

    def test_split_nodes_delimiter_multiple_matches(self):
        node = TextNode(
            "This is text with a *italic* word. And another *italic* word.",
            TEXT_TYPE_TEXT,
        )
        new_nodes = split_nodes_delimiter([node], "*", TEXT_TYPE_ITALIC)
        expected_nodes = [
            TextNode("This is text with a ", TEXT_TYPE_TEXT),
            TextNode("italic", TEXT_TYPE_ITALIC),
            TextNode(" word. And another ", TEXT_TYPE_TEXT),
            TextNode("italic", TEXT_TYPE_ITALIC),
            TextNode(" word.", TEXT_TYPE_TEXT),
        ]
        self.assertListEqual(expected_nodes, new_nodes)

    def test_split_nodes_delimiter_empty_nodes(self):
        node = TextNode("*italic**italic2*", TEXT_TYPE_TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TEXT_TYPE_ITALIC)
        expected_nodes = [
            TextNode("italic", TEXT_TYPE_ITALIC),
            TextNode("italic2", TEXT_TYPE_ITALIC),
        ]
        self.assertListEqual(expected_nodes, new_nodes)

    def test_split_nodes_delimiter_invalid_markdown(self):
        node = TextNode("This is text with a code block` word", TEXT_TYPE_TEXT)
        with self.assertRaises(ValueError) as context_manager:
            split_nodes_delimiter([node], "`", TEXT_TYPE_CODE)
        the_exception = context_manager.exception
        expected_message = (
            "Invalid markdown syntax, missing closing '`' "
            "delimiter: 'This is text with a code block` word'"
        )
        self.assertEqual(type(the_exception), ValueError)
        self.assertEqual(str(the_exception), expected_message)

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        markdown_images = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            markdown_images,
        )

    def test_extract_markdown_images_no_matches(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        markdown_links = extract_markdown_images(text)
        self.assertListEqual([], markdown_links)

    def test_extract_markdown_images_one_match(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        markdown_images = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            markdown_images,
        )

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        markdown_links = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            markdown_links,
        )

    def test_extract_markdown_links_no_matches(self):
        text = "This is text with a link <to boot dev>(https://www.boot.dev) and <to youtube>(https://www.youtube.com/@bootdotdev)"
        markdown_links = extract_markdown_links(text)
        self.assertListEqual([], markdown_links)

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TEXT_TYPE_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TEXT_TYPE_TEXT),
                TextNode("to boot dev", TEXT_TYPE_LINK, "https://www.boot.dev"),
                TextNode(" and ", TEXT_TYPE_TEXT),
                TextNode(
                    "to youtube", TEXT_TYPE_LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an image ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TEXT_TYPE_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an image ", TEXT_TYPE_TEXT),
                TextNode("to boot dev", TEXT_TYPE_IMAGE, "https://www.boot.dev"),
                TextNode(" and ", TEXT_TYPE_TEXT),
                TextNode(
                    "to youtube", TEXT_TYPE_IMAGE, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_image_no_matches(self):
        node = TextNode(
            "This is text with an image [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TEXT_TYPE_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_nodes_image_no_surrounding_text(self):
        node = TextNode(
            "![to boot dev](https://www.boot.dev)![to youtube](https://www.youtube.com/@bootdotdev)",
            TEXT_TYPE_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("to boot dev", TEXT_TYPE_IMAGE, "https://www.boot.dev"),
                TextNode(
                    "to youtube", TEXT_TYPE_IMAGE, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_image_trailing_text(self):
        node = TextNode(
            "![to boot dev](https://www.boot.dev)followed by this!",
            TEXT_TYPE_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("to boot dev", TEXT_TYPE_IMAGE, "https://www.boot.dev"),
                TextNode("followed by this!", TEXT_TYPE_TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TEXT_TYPE_TEXT),
                TextNode("text", TEXT_TYPE_BOLD),
                TextNode(" with an ", TEXT_TYPE_TEXT),
                TextNode("italic", TEXT_TYPE_ITALIC),
                TextNode(" word and a ", TEXT_TYPE_TEXT),
                TextNode("code block", TEXT_TYPE_CODE),
                TextNode(" and an ", TEXT_TYPE_TEXT),
                TextNode(
                    "obi wan image", TEXT_TYPE_IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TEXT_TYPE_TEXT),
                TextNode("link", TEXT_TYPE_LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_text_to_textnodes_no_matches(self):
        text = "This is text with an italic word and a code block and an obi wan image https://i.imgur.com/fJRm4Vk.jpeg and a link https://boot.dev"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode(
                    "This is text with an italic word and a code block and an obi wan image https://i.imgur.com/fJRm4Vk.jpeg and a link https://boot.dev",
                    TEXT_TYPE_TEXT,
                )
            ],
            nodes,
        )

    def test_text_to_textnodes_no_empty(self):
        text = ""
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [],
            nodes,
        )
