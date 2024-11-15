import re
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            node_splits = node.text.split(delimiter)
            if len(node_splits) % 2 == 0:
                raise Exception("Invalid Markdown syntax: no matching closing delimiter found")
            for index, split in enumerate(node_splits):
                if split == '':
                    continue
                if index % 2 == 0:
                    new_nodes.append(TextNode(split, TextType.TEXT, None))
                else:
                    new_nodes.append(TextNode(split, text_type, None))
        else:
            new_nodes.append(node)

    return new_nodes


def extract_markdown_images(text):
    images = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return images


def extract_markdown_links(text):
    links = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return links


def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            old_node_split = re.split(r"(!\[.*?\]\(.*?\))", old_node.text)

            for index, split in enumerate(old_node_split):
                if split == "":
                    continue
                if index % 2 == 0:
                    new_nodes.append(TextNode(split, TextType.TEXT, None))
                else:
                    image_text_url = extract_markdown_images(split)[0]
                    new_nodes.append(TextNode(image_text_url[0], TextType.IMAGE, image_text_url[1]))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            old_node_split = re.split(r"((?<!!)\[.*?\]\(.*?\))", old_node.text)

            for index, split in enumerate(old_node_split):
                if split == "":
                    continue
                if index % 2 == 0:
                    new_nodes.append(TextNode(split, TextType.TEXT, None))
                else:
                    link_text_url = extract_markdown_links(split)[0]
                    new_nodes.append(TextNode(link_text_url[0], TextType.LINK, link_text_url[1]))

    return new_nodes


def text_to_textnodes(text):
    nodes_list = [TextNode(text, TextType.TEXT, None)]

    nodes_list = split_nodes_delimiter(nodes_list, "**", TextType.BOLD)
    nodes_list = split_nodes_delimiter(nodes_list, "*", TextType.ITALIC)
    nodes_list = split_nodes_delimiter(nodes_list, "`", TextType.CODE)
    nodes_list = split_nodes_image(nodes_list)
    nodes_list = split_nodes_link(nodes_list)

    return nodes_list
