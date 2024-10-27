import os
import shutil

from textnode import TextNode


def copy_content(source_directory: str, target_directory: str):
    if not os.path.isdir(source_directory):
        raise ValueError(f"Invalid source directory: {source_directory}")
    if os.path.isdir(target_directory):
        shutil.rmtree(target_directory)

    items = os.listdir(source_directory)
    os.mkdir(target_directory)

    for item in items:
        source_item = os.path.join(source_directory, item)
        target_item = os.path.join(target_directory, item)
        if os.path.isfile(source_item):
            print(f"copying file {source_item} to {target_item}")
            shutil.copy(source_item, target_item)
        else:
            print(f"creating directory {source_item} to {target_item}")
            copy_content(source_item, target_item)


def main():
    # text_node = TextNode("A textnode", "italic", "https://mywebsite.com")
    text_node = TextNode("click me", "link", "http://clickme.com")
    print(text_node)


# main()


if __name__ == "__main__":
    copy_content("../static", "../public")
