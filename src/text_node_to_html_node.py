from htmlnode import LeafNode
from textnode import TextNode, TextType

def text_node_to_html_node(text_node):
    available_types = {"text": [None, text_node.text], 
                       "bold": ["b", text_node.text], 
                       "italic": ["i", text_node.text], 
                       "code": ["code", text_node.text],
                       "link": ["a", text_node.text, {"href": text_node.url}],
                       "image": ["img", f'', {"src": text_node.url, "alt": text_node.text}]
    }

    if text_node.text_type.value not in available_types:
        raise Exception("Invalid TextNode: not one of the allowed types")

    return LeafNode(*available_types[text_node.text_type.value]) 
