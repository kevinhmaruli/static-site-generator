import unittest
from htmlnode import ParentNode, LeafNode, HTMLNode
from textnode import TextNode, TextType
from block_markdown import markdown_to_blocks, block_to_block_type
from markdown_to_html_node import markdown_to_html_node

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """# THIS IS AN EXAMPLE

This is just an example, you
are supposed to be able to turn this into html.

> Ask not what you can do for your country
> but what your country can do
> for you!

## Here are some things you need to understand

* first thing
* second thing
* third thing
"""
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.to_html(),
f"<div><h1>THIS IS AN EXAMPLE</h1><p>This is just an example, you\nare supposed to be able to turn this into html.</p><blockquote>Ask not what you can do for your country but what your country can do for you!</blockquote><h2>Here are some things you need to understand</h2><ul><li>first thing</li><li>second thing</li><li>third thing</li></ul></div>"
)

if __name__ == "__main__":
    unittest.main()

