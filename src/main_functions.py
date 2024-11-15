import os
import shutil
from block_markdown import (
    markdown_to_blocks
)
# from htmlnode import HTMLNode
from markdown_to_html_node import markdown_to_html_node 


def extract_title(markdown):
    lines = markdown_to_blocks(markdown)
    for line in lines:
        if line.strip().startswith('# '):
            return line.strip('# ')
    raise Exception('No h1 header found')


def copy_static(source, destination):
    """Copies all the content from a source directory to a destination
    directory recursively."""
    # Create a fresh copy of the destination folder while deleting the old one.
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)

    # Loop over every single file and/or directory in the source:
    for content in os.listdir(source):
        path_to_content = os.path.join(source, content)

        # If content is a file, directly copy it to the destination directory:
        if os.path.isfile(path_to_content):
            shutil.copy(path_to_content, destination)
        else: # If content is a subdirectory, recursively call the function
            new_subdirectory = os.path.join(destination, content)
            copy_static(path_to_content, new_subdirectory)


def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')

    f = open(from_path)
    content = f.read()
    f.close()

    f = open(template_path)
    template = f.read()
    f.close()

    content_html = markdown_to_html_node(content).to_html()
    title = extract_title(content)
    page_html = template.replace('{{ Title }}', title).replace('{{ Content }}', content_html)

    dest_dirname = os.path.dirname(dest_path)
    if dest_dirname != '':
        os.makedirs(dest_dirname, exist_ok=True)

    page = open(dest_path, 'w')
    page.write(page_html)
    page.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    items = os.listdir(dir_path_content)

    for item in items:
        print(item)
        item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(item_path) and item.endswith('.md'):
            dest_path = os.path.join(dest_dir_path, item[:-3] + '.html')
            generate_page(item_path, template_path, dest_path)
        else:
            dest_path = os.path.join(dest_dir_path, item)
            os.makedirs(dest_path)
            generate_pages_recursive(item_path, template_path, dest_path)
