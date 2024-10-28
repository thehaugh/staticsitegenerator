from os.path import isdir, dirname, isfile
from os import listdir, makedirs
import os
from shutil import rmtree

from block_markdown import extract_title, markdown_to_html_node
from copystatic import copy_content

SOURCE_DIR = "./static"
TARGET_DIR = "./public"


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as _file:
        markdown = _file.read()

    with open(template_path, "r") as _file:
        template = _file.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    if not isdir(dirname(dest_path)):
        makedirs(dirname(dest_path))

    with open(dest_path, "w") as _file:
        _file.write(template)


def generate_pages_recursive(
    dir_content_path: str, template_path: str, dest_dir_path: str
):
    entries = listdir(dir_content_path)

    for entry in entries:
        source = os.path.join(dir_content_path, entry)
        dest = os.path.join(dest_dir_path, entry)
        if isfile(source):
            if entry.endswith(".md"):
                generate_page(source, template_path, dest[:-3] + ".html")
        else:
            generate_pages_recursive(source, template_path, dest)


def main():
    if isdir(TARGET_DIR):
        print(f"Removing directory {TARGET_DIR}")
        rmtree(TARGET_DIR)
    copy_content(SOURCE_DIR, TARGET_DIR)
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
