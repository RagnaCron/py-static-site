import os
import pathlib
import shutil

from src.blocktype import markdown_to_html_node


def create_sub_tree_from_dir(from_path: str = "static", to_path: str = "public"):
    directory = os.listdir(from_path)
    for item in directory:
        curr_path = os.path.join(from_path, item)
        if os.path.isfile(curr_path):
            abs_path = os.path.abspath(curr_path)
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


def extract_title(markdown: str) -> str:
    h1 = markdown.split("\n", maxsplit=1)
    if len(h1) > 1 and h1[0].startswith("# "):
        return h1[0][2:]
    raise ValueError("markdown does not contain a valid title (h1)")


def generate_page(from_path: str, template_path: str, to_path: str):
    print(f"Generating page from {from_path} to {to_path} using template {template_path}")
    content = ""
    with open(from_path, "r") as f:
        content = f.read()
    with open(template_path, "r") as f:
        template = f.read()

    title = extract_title(content)
    html = markdown_to_html_node(content).to_html()
    rendered = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    with open(to_path, "w") as f:
        f.write(rendered)


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    contents = os.listdir(dir_path_content)
    for content in contents:
        path = os.path.join(dir_path_content, content)
        if os.path.isdir(path):
            dest_path = os.path.join(dest_dir_path, content)
            os.makedirs(os.path.abspath(dest_path), exist_ok=True)
            generate_pages_recursive(path, template_path, dest_path)
        else:
            basename = pathlib.Path(content).stem
            generate_page(path, template_path, os.path.join(dest_dir_path, basename + ".html"))


def main():
    copy_static_files_to("public")
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
