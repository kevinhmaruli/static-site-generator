import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from text_node_to_html_node import text_node_to_html_node

class TestHTMLNode(unittest.TestCase):
    def test1(self):
        node1 = HTMLNode("a", "boot.dev website", props={"href": "https://www.boot.dev"})
        expected_props = ' href="https://www.boot.dev"'
        self.assertEqual(node1.props_to_html(), expected_props)

    def test2(self):
        node1 = HTMLNode("a", "link to google", props={"href": "https://google.com", "target": "_blank",})
        expected_props = ' href="https://google.com" target="_blank"'
        self.assertEqual(node1.props_to_html(), expected_props)

    def test3(self):
        node1 = HTMLNode("img", props={"src": "picture.jpeg", "alt": "this is a picture"})
        expected_props = ' src="picture.jpeg" alt="this is a picture"'
        self.assertEqual(node1.props_to_html(), expected_props)

    def test4(self):
        node1 = HTMLNode("img")
        expected_props = ''
        self.assertEqual(node1.props_to_html(), expected_props)

    def test5(self):
        node = HTMLNode("b", "hello there", None, None)
        self.assertEqual(node.__repr__(), "HTMLNode(b, hello there, children: None, None)")

    def test6(self):
        node1 = LeafNode("p", "This is a paragraph of text.")
        expected_render = '<p>This is a paragraph of text.</p>'
        self.assertEqual(node1.to_html(), expected_render)

    def test7(self):
        node1 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected_render = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node1.to_html(), expected_render)

    def test8(self):
        node1 = LeafNode("img", None, {"src": "example_picture.jpeg", "alt": "this is a picture"})
        try:
            node1.to_html()
            self.assertEqual(0, 1)
        except ValueError:
            self.assertEqual(1, 1)

    def test9(self):
        node1 = LeafNode(None, "This is a text", {"href": "https://www.google.com"})
        expected_render = 'This is a text'
        self.assertEqual(node1.to_html(), expected_render)

    def test_parent_node(self):
        node = ParentNode(
                "p",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_parent_node_nested(self):
        node = ParentNode("div",
                [
                    ParentNode("p", 
                                [
                                    LeafNode("b", "Bold text"),
                                    LeafNode(None, "Normal text"),
                                    LeafNode("i", "italic text"),
                                    LeafNode(None, "Normal text"),
                                ],
                                {"color": "blue"}
                    ),
                    LeafNode("a", "this here is a link!", {"href": "https://google.com"}),
                    LeafNode("i", "italic text again")
                ],
                {"prop": "some value"}
        )
        self.assertEqual(node.to_html(), '<div prop="some value"><p color="blue"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><a href="https://google.com">this here is a link!</a><i>italic text again</i></div>')

    def test_parent_node_multiple_nested(self):
        node = ParentNode("div",
                [
                    ParentNode("p", 
                                [
                                    LeafNode("b", "Bold text"),
                                    LeafNode(None, "Normal text"),
                                    LeafNode("i", "italic text"),
                                    LeafNode(None, "Normal text"),
                                ],
                                {"color": "blue"}
                    ),
                    ParentNode("p", 
                                [
                                    LeafNode("b", "Bold text"),
                                    LeafNode(None, "Normal text"),
                                    LeafNode("i", "italic text"),
                                    LeafNode(None, "Normal text"),
                                ],
                                {"color": "blue"}
                    ),
                    LeafNode("a", "this here is a link!", {"href": "https://google.com"}),
                    LeafNode("i", "italic text again")
                ],
                {"prop": "some value"}
        )
        self.assertEqual(node.to_html(), '<div prop="some value"><p color="blue"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><p color="blue"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><a href="https://google.com">this here is a link!</a><i>italic text again</i></div>')

    def test_parent_node_multiple_nested_two_levels(self):
        node = ParentNode("div",
                [
                    ParentNode("p", 
                                [
                                    
                                    ParentNode("p", 
                                                [
                                                    LeafNode("b", "Bold text"),
                                                    LeafNode(None, "Normal text"),
                                                    LeafNode("i", "italic text"),
                                                    LeafNode(None, "Normal text"),
                                                ],
                                                {"color": "blue"}
                                    ),

                                    LeafNode(None, "Normal text"),
                                    LeafNode("i", "italic text"),
                                    LeafNode(None, "Normal text"),
                                ],
                                {"color": "blue"}
                    ),
                    ParentNode("p", 
                                [
                                    LeafNode("b", "Bold text"),
                                    LeafNode(None, "Normal text"),
                                    LeafNode("i", "italic text"),
                                    LeafNode(None, "Normal text"),
                                ],
                                {"color": "blue"}
                    ),
                    LeafNode("a", "this here is a link!", {"href": "https://google.com"}),
                    LeafNode("i", "italic text again")
                ],
                {"prop": "some value"}
        )
        self.assertEqual(node.to_html(), '<div prop="some value"><p color="blue"><p color="blue"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>Normal text<i>italic text</i>Normal text</p><p color="blue"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><a href="https://google.com">this here is a link!</a><i>italic text again</i></div>')

    def test_parent_node_no_children(self):
        node = ParentNode("div", None, {"prop": "some value"})
        try:
            node.to_html()
            self.assertEqual(1, 0)
        except ValueError:
            self.assertEqual(1, 1)

    def test_parent_node_no_tag(self):
        node = ParentNode(None, [LeafNode("a", "link", {"href": "http"})], {"prop": "some value"})
        try:
            node.to_html()
            self.assertEqual(1, 0)
        except ValueError:
            self.assertEqual(1, 1)

    def test_text_to_html_node(self):
        text_node = TextNode("hello there", TextType.BOLD)
        self.assertEqual(text_node_to_html_node(text_node).to_html(), "<b>hello there</b>")

    def test_image_text_node_to_html_node_function(self):
        text_node = TextNode("this is the alt text", TextType.IMAGE, "./picture.jpeg")
        self.assertEqual(text_node_to_html_node(text_node).to_html(), '<img src="./picture.jpeg" alt="this is the alt text"></img>')


if __name__ == "__main__":
    unittest.main()
