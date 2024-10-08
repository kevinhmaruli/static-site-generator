import unittest

from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_uneq(self):
        node1 = TextNode("This is text node 1", "bold")
        node2 = TextNode("This is text node 2", "bold")
        self.assertNotEqual(node1, node2)

    def test_uneq2(self):
        node1 = TextNode("This is text node 1", "bold")
        node2 = TextNode("This is text node 1", "italic")
        self.assertNotEqual(node1, node2)

    def test_uneq3(self):
        node1 = TextNode("This is text node 1", "bold")
        node2 = TextNode("This is text node 1", "bold", None)
        self.assertEqual(node1, node2)

if __name__ == "__main__":
    unittest.main()
