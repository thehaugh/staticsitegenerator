from collections.abc import Callable
from textnode import (
    TEXT_TYPE_BOLD,
    TEXT_TYPE_CODE,
    TEXT_TYPE_IMAGE,
    TEXT_TYPE_ITALIC,
    TEXT_TYPE_LINK,
    TextNode,
    TEXT_TYPE_TEXT,
)
import re


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: str
) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TEXT_TYPE_TEXT:
            new_nodes.append(old_node)
            continue

        split_text = old_node.text.split(delimiter)
        num_fields = len(split_text)
        if num_fields % 2 == 0:
            raise ValueError(
                (
                    f"Invalid markdown syntax, missing closing '{delimiter}' "
                    f"delimiter: '{old_node.text}'"
                )
            )
        for index, field in enumerate(split_text):
            if field == "":
                continue
            elif index % 2 == 0:
                new_nodes.append(TextNode(field, TEXT_TYPE_TEXT))
            else:
                new_nodes.append(TextNode(field, text_type))
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"[^!]\[(.*?)\]\((.*?)\)", text)
    return matches


def split_nodes_extractor(
    old_nodes: list[TextNode],
    text_type: str,
    extract_func: Callable[[str], list[tuple[str, str]]],
    split_string: str,
) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TEXT_TYPE_TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text

        elements = extract_func(original_text)
        if len(elements) == 0:
            new_nodes.append(old_node)
            continue

        for element in elements:
            sections = original_text.split(
                split_string.format(element[0], element[1]), 1
            )
            if len(sections) != 2:
                raise ValueError(f"Invalid markdown, {text_type} section not closed")
            original_text = sections[1]
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TEXT_TYPE_TEXT))
            new_nodes.append(TextNode(element[0], text_type, url=element[1]))

        if original_text != "":
            new_nodes.append(TextNode(original_text, TEXT_TYPE_TEXT))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes_extractor(
        old_nodes, TEXT_TYPE_IMAGE, extract_markdown_images, "![{}]({})"
    )


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes_extractor(
        old_nodes, TEXT_TYPE_LINK, extract_markdown_links, "[{}]({})"
    )


def text_to_textnodes(text: str) -> list[TextNode]:
    text_nodes = [TextNode(text, TEXT_TYPE_TEXT)]
    text_nodes = split_nodes_delimiter(text_nodes, "**", TEXT_TYPE_BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "*", TEXT_TYPE_ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TEXT_TYPE_CODE)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes


if __name__ == "__main__":
    node = TextNode("a ` text node", "text")
    split_nodes_delimiter([node], "`", "code")
