from block_markdown import (
    markdown_to_blocks,
    block_to_block_type
)
from text_node_to_html_node import text_node_to_html_node
from inline_markdown import text_to_textnodes
from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType

# split the markdown into a blocks (in a list)
# for each block, create an appropriate htmlnode (parent node) and its children
#   - the parent is easy...
#   - the children... first you have to get rid of the parent markdown tags
#     then feed the text into the text_to_textnodes function
#     ^^^^ This will the job of the text_to_children function (it takes a block
#          and gives a list of html nodes that represent the inline markdown
#     then create children nodes out of those... (maybe use map...)


def list_items_textnodes_to_html_nodes(textnodes):
    list_items_html_nodes = []
    for item in textnodes:
        list_items_html_nodes.append(list(map(text_node_to_html_node, item)))
    return list_items_html_nodes


def text_to_children(text):
    type = block_to_block_type(text)

    if type == "heading":
        ctext = text.lstrip("# ")
        textnodes = text_to_textnodes(ctext)
        children = [text_node_to_html_node(textnode) for textnode in textnodes]
    elif type == "code":
        ctext = text.strip("`\n")
        textnodes = text_to_textnodes(ctext)
        children = [text_node_to_html_node(textnode) for textnode in textnodes]
        children = [ParentNode("code", children, None)]
    elif type == "quote":
        list_items = text.split("\n")
        just_text = [list_item.lstrip(">").lstrip() for list_item in list_items]
        quote_str = ""
        for item in just_text:
            quote_str += item + " "
        quote_str = quote_str.rstrip()
        textnodes = text_to_textnodes(quote_str) 
        children = list(map(text_node_to_html_node, textnodes))
    elif type == "unordered_list":
        list_items = text.split("\n")
        just_text = [list_item.lstrip("*-").lstrip() for list_item in list_items]
        textnodes = list(map(text_to_textnodes, just_text))
        htmlnodes = list_items_textnodes_to_html_nodes(textnodes)
        children = [ParentNode("li", nodes, None) for nodes in htmlnodes]
    elif type == "ordered_list":
        list_items = text.split("\n")
        just_text = [list_item.lstrip("0123456789.").lstrip() for list_item in list_items]
        textnodes = list(map(text_to_textnodes, just_text))
        htmlnodes = list_items_textnodes_to_html_nodes(textnodes)
        children = [ParentNode("li", node, None) for node in htmlnodes]
    else:
        textnodes = text_to_textnodes(text)
        children = [text_node_to_html_node(textnode) for textnode in textnodes]

    return children


def block_to_html_tag(block):
    block_type = block_to_block_type(block)

    match block_type:
        case "heading":
            if block.startswith("######"):
                return "h6"
            elif block.startswith("#####"):
                return "h5"
            elif block.startswith("####"):
                return "h4"
            elif block.startswith("###"):
                return "h3"
            elif block.startswith("##"):
                return "h2"
            else:
                return "h1"
        case "quote":
            return "blockquote"
        case "unordered_list":
            return "ul"
        case "ordered_list":
            return "ol"
        case "code":
            return "pre"
        case "paragraph":
            return "p"


def block_to_html_node(block):
    parent_tag = block_to_html_tag(block)
    children = text_to_children(block)
    return ParentNode(parent_tag, children, None)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = list(map(block_to_html_node, blocks))
    return ParentNode("div", children, None)

