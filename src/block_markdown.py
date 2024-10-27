import re
from enum import Enum
from functools import reduce

from parentnode import ParentNode
from leafnode import LeafNode
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ORDERED_LIST = "ordered_list"
    UNORDERED_LIST = "unordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        block = block.strip()
        if block == "":
            continue
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block: str) -> BlockType:
    if block.startswith("#"):
        if block.startswith("#"):
            if re.match(r"#{1,6} ", block):
                return BlockType.HEADING
        return BlockType.PARAGRAPH

    if block.startswith("```"):
        if block.endswith("```"):
            return BlockType.CODE
        return BlockType.PARAGRAPH

    lines = block.split("\n")
    if block.startswith(">"):
        for line in lines[1:]:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if block.startswith("* "):
        for line in lines[1:]:
            if not line.startswith("* "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    if block.startswith("- "):
        for line in lines[1:]:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    if block.startswith("1. "):
        for index, line in enumerate(lines[1:]):
            if not line.startswith(str(index + 2) + ". "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def block_to_html_node(block: str) -> ParentNode:
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return ParentNode(
                tag="p", children=text_to_children(block.replace("\n", " "))
            )
        case BlockType.QUOTE:
            block = reduce(
                lambda x, y: x + re.sub(r"^>", "", y).strip() + " ",
                block.split("\n"),
                "",
            ).strip()
            return ParentNode(tag="blockquote", children=text_to_children(block))
        case BlockType.CODE:
            return ParentNode(
                tag="pre",
                children=[
                    ParentNode(
                        tag="code",
                        children=text_to_children(
                            re.sub(r"^```|```$", "", block).strip()
                        ),
                    )
                ],
            )
        case BlockType.ORDERED_LIST:
            children = map(
                lambda x: ParentNode(
                    tag="li", children=text_to_children(x[2:].strip())
                ),
                block.split("\n"),
            )
            return ParentNode(tag="ol", children=list(children))
        case BlockType.UNORDERED_LIST:
            children = map(
                lambda x: ParentNode(
                    tag="li", children=text_to_children(x[2:].strip())
                ),
                block.split("\n"),
            )
            return ParentNode(tag="ul", children=list(children))
        case BlockType.HEADING:
            match = re.match(r"^(#{1,6}) ", block)
            header_num = len(match.group(1))
            return ParentNode(
                tag=f"h{header_num}", children=text_to_children(block[header_num + 1 :])
            )
        case _:
            raise ValueError("Invalid block type")


def text_to_children(text: str) -> list[LeafNode]:
    children = map(lambda x: text_node_to_html_node(x), text_to_textnodes(text))
    return list(children)


def markdown_to_html_node(markdown: str) -> ParentNode:
    children = []
    markdown_blocks = markdown_to_blocks(markdown)

    for block in markdown_blocks:
        children.append(block_to_html_node(block))

    return ParentNode(tag="div", children=children)


if __name__ == "__main__":
    print(BlockType.PARAGRAPH)
