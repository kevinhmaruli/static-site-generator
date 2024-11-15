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

class TestInlineMarkdown(unittest.TestCase):
    def test_split_delimitter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, 
                         [
                            TextNode("This is text with a ", TextType.TEXT),
                            TextNode("code block", TextType.CODE),
                            TextNode(" word", TextType.TEXT),
                         ]
        )

    def test_split_delimitter_bold(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, 
                         [
                            TextNode("This is text with a ", TextType.TEXT),
                            TextNode("bold block", TextType.BOLD),
                            TextNode(" word", TextType.TEXT),
                         ]
        )

    def test_split_delimitter_two(self):
        node = TextNode("This is text with a **bold block** and a *italic block*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertEqual(new_new_nodes, 
                         [
                            TextNode("This is text with a ", TextType.TEXT),
                            TextNode("bold block", TextType.BOLD),
                            TextNode(" and a ", TextType.TEXT),
                            TextNode("italic block", TextType.ITALIC),
                         ]
        )


class TestExtractImagesAndLinks(unittest.TestCase):
    def test_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_no_images(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [])

    def test_links(self):
        text = "This is text with a link [rick roll](https://i.imgur.com/aKaOqIh.gif) and an image ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_links(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif")])


class TestSplitImagesAndLinks(unittest.TestCase):
    def test_split_images(self):
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT, None)
        self.assertEqual(split_nodes_image([node]), 
                         [TextNode("This is text with a ", TextType.TEXT, None), 
                          TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                          TextNode(" and ", TextType.TEXT, None), 
                          TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_split_no_images(self):
        node = TextNode("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT, None)
        self.assertEqual(split_nodes_image([node]), 
                         [TextNode("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT, None)]) 

    def test_split_image_but_with_links(self):
        node = TextNode("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT, None)
        self.assertEqual(split_nodes_image([node]), 
                         [TextNode("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and ", TextType.TEXT, None), 
                          TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        self.assertEqual(split_nodes_link([node]),
                        [
                             TextNode("This is text with a link ", TextType.TEXT),
                             TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                             TextNode(" and ", TextType.TEXT),
                             TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                        ]
        )


class TestMarkdownTextToTextNode(unittest.TestCase):
    def test_simple_text(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text_node = text_to_textnodes(text)
        self.assertEqual(text_node,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )

    def test_error(self):
        text = "This is **text* with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        try:
            text_node = text_to_textnodes(text)
            self.assertEqual(1, 0)
        except Exception:
            self.assertEqual(1, 1)

    def test_simple_text2(self):
        text = "This is text without anything"
        text_node = text_to_textnodes(text)
        self.assertEqual(text_node,
            [TextNode("This is text without anything", TextType.TEXT)]
        )

if __name__ == "__main__":
    unittest.main()

