from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    markdown_to_html_node,
)
from unittest import TestCase


class TestBlockMarkdown(TestCase):

    def test_markdown_to_blocks(self):
        markdown = (
            "# This is a heading\n"
            "\n"
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n"
            "\n"
            "* This is the first list item in a list block\n"
            "* This is a list item\n"
            "* This is another list item\n"
        )

        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
            ],
            blocks,
        )

    def test_markdown_to_blocks_extra_spaces(self):
        markdown = (
            "# This is a heading\n"
            "\n"
            "\n"
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n"
            "\n"
            "\n"
            "\n"
            "\n"
            "\n"
            "* This is the first list item in a list block\n"
            "* This is a list item\n"
            "\n"
            "* This is another list item\n"
            "\n"
            "\n"
        )

        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item",
                "* This is another list item",
            ],
            blocks,
        )

    def test_markdown_to_blocks_empty_string(self):
        markdown = ""
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual([], blocks)

    def test_block_to_block_type_heading(self):
        block = "# test"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.HEADING, block_type)

    def test_block_to_block_type_heading_6_hashes(self):
        block = "###### test"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.HEADING, block_type)

    def test_block_to_block_type_heading_7_hashes(self):
        block = "####### test"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_block_to_block_type_code(self):
        block = "``` print(hello world)\n# this is a test```"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.CODE, block_type)

    def test_block_to_block_type_quote(self):
        block = "> To be or not to be,\n> that is the question\n> starts right."
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.QUOTE, block_type)

    def test_block_to_block_type_code_invalid(self):
        block = "``` print(hello world)\n# this is a test```test"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_block_to_block_type_quote_invalid_last_line(self):
        block = "> To be or not to be,\n> that is the question\ndoes not start right."
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_block_to_block_type_unordered_list_star(self):
        block = "* item 1\n* item 2\n* item 3"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.UNORDERED_LIST, block_type)

    def test_block_to_block_type_unordered_list_dash(self):
        block = "- item 1\n- item 2\n- item 3"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.UNORDERED_LIST, block_type)

    def test_block_to_block_type_ordered_list(self):
        block = "1. item 1\n2. item 2\n3. item3"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.ORDERED_LIST, block_type)

    def test_block_to_block_type_ordered_list_invalid_start(self):
        block = "2. item 1\n3. item 2\n4. item3"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_markdown_to_html_node_header_list(self):
        markdown = """
# The **title**.

1. *This* is a list.
2. with numbers.
3. and a link! [link]("www.test.com")
"""
        expected_html = '<div><h1>The <b>title</b>.</h1><ol><li><i>This</i> is a list.</li><li>with numbers.</li><li>and a link! <a href=""www.test.com"">link</a></li></ol></div>'
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(expected_html, html_node.to_html())

    def test_markdown_to_html_node_quote_code(self):
        markdown = """
## A second title.

> Every man *dies*, not every man really *lives*.
> -William Wallace.

```
print("hello world!")
```

A nice image: ![nice](images/nice.jpg)
"""
        expected_html = '<div><h2>A second title.</h2><blockquote>Every man <i>dies</i>, not every man really <i>lives</i>. -William Wallace.</blockquote><pre><code>print("hello world!")</code></pre><p>A nice image: <img src="images/nice.jpg" alt="nice"></img></p></div>'
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(expected_html, html_node.to_html())
