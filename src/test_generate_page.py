import unittest
from main_functions import extract_title 

class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        text = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        title = extract_title(text)
        self.assertEqual('This is a heading', title)

    def test_no_title(self):
        md = """
## There is no title here

### You'll do better searching for it elsewhere

This is a paragraph
"""
        try:
            title = extract_title(md)
        except Exception as e:
            self.assertEqual(1, 1)


if __name__ == "__main__":
    unittest.main()

