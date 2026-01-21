import os
import shutil


def create_sub_tree_from_dir(from_path: str = "static", to_path: str = "public"):
    directory = os.listdir(from_path)
    for item in directory:
        curr_path = os.path.join(from_path, item)
        if os.path.isfile(curr_path):
            abs_path = os.path.abspath(os.path.join(from_path, item))
            shutil.copy(abs_path, to_path)
        else:
            abs_path = os.path.abspath(os.path.join(to_path, item))
            os.mkdir(abs_path)
            create_sub_tree_from_dir(curr_path, abs_path)


def copy_static_files_to(path: str):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
    create_sub_tree_from_dir("static", path)


def main():
    copy_static_files_to("public")


if __name__ == "__main__":
    main()
