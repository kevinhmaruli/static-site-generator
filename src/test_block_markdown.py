import unittest
from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)
from block_markdown import markdown_to_blocks, block_to_block_type

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        markdown_blocks = markdown_to_blocks(text)
        self.assertEqual(markdown_blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                """* This is the first list item in a list block
* This is a list item
* This is another list item"""
            ]
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type(self):
        text = """
# This is a heading

#### heading number two

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item

```
this is code
```

> This is a quote
> continuation of the quote

> wrong quote
# wrong
"""

        blocks = markdown_to_blocks(text) 
        block_types = [block_to_block_type(block) for block in blocks]
        self.assertEqual(block_types, ["heading", "heading", "paragraph", "unordered_list", "code", "quote", "paragraph"])

    def test_ordered_list_correct(self):
        list_block = """1. list item numero uno
2. list item numero dos
3. list item numero tres"""
        
        self.assertEqual(block_to_block_type(list_block), "ordered_list")

    def test_ordered_list_wrong(self):
        list_block = """1. list item numero uno
3. list item numero dos
3. list item numero tres"""
        
        self.assertEqual(block_to_block_type(list_block), "paragraph")

    def test_unordered_list(self):
        list_block_right = """* list item numero uno
* list item numero dos
* list item numero tres"""
        
        list_block_wrong = """- list item numero uno
* list item numero dos
* list item numero tres"""
        self.assertEqual(block_to_block_type(list_block_right), "unordered_list")
        self.assertEqual(block_to_block_type(list_block_wrong), "paragraph")


if __name__ == "__main__":
    unittest.main()

