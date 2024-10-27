from os.path import isdir, dirname
from os import makedirs
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
        makedirs(dest_path)

    with open(dest_path, "w") as _file:
        _file.write(template)


def main():
    if isdir(TARGET_DIR):
        print(f"Removing directory {TARGET_DIR}")
        rmtree(TARGET_DIR)
    copy_content(SOURCE_DIR, TARGET_DIR)
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
