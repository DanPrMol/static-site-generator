from textnode import *
from block_markdown import *
from htmlnode import *
import os
import shutil

def main():
    clean_dir("./public")
    rec_copy("./static", "./public")
    generate_pages_recursive("./content", "./template.html", "./public")

def clean_dir(dir):
    if os.path.exists(dir):
        for item in os.listdir(dir):
            item_path = os.path.join(dir, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            else:
                shutil.rmtree(item_path)

def rec_copy(source, destination):
    if not os.path.exists(destination):
        os.mkdir(destination)
    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)
        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
        else:
            rec_copy(source_path, destination_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    with open(template_path, "r") as f:
        template = f.read()
    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    with open(dest_path, "w") as f:
        f.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    os.makedirs(dest_dir_path, exist_ok=True)
    for entry in os.listdir(dir_path_content):
        input_path = os.path.join(dir_path_content, entry)
        if os.path.isdir(input_path):
            output_path = os.path.join(dest_dir_path, entry)
            generate_pages_recursive(input_path, template_path, output_path)
        else:
            file_without_ext, _ = os.path.splitext(entry)
            html_file = file_without_ext + '.html'
            html_path = os.path.join(dest_dir_path, html_file)
            generate_page(input_path, template_path, html_path)

if __name__ == "__main__":
    main()