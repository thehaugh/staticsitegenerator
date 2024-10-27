from os.path import isdir
from shutil import rmtree

from copystatic import copy_content

SOURCE_DIR = "./static"
TARGET_DIR = "./public"


def main():
    if isdir(TARGET_DIR):
        print(f"Removing directory {TARGET_DIR}")
        rmtree(TARGET_DIR)
    copy_content(SOURCE_DIR, TARGET_DIR)


main()


if __name__ == "__main__":
    pass
