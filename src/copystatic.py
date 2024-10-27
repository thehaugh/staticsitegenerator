import os
import shutil


def copy_content(source_directory: str, target_directory: str):
    if not os.path.isdir(source_directory):
        raise ValueError(f"Invalid source directory: {source_directory}")
    if os.path.isdir(target_directory):
        print(f"Removing directory {target_directory}")
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
            copy_content(source_item, target_item)
