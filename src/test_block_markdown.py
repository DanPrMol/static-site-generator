import unittest

from block_markdown import *

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
            ],
            blocks,
        )

    def test_remove_empty_blocks(self):
        markdown = "# This is a heading\n\n\n\n   This is a paragraph of text. It has some **bold** and *italic* words inside of it."
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            ],
            blocks,
        )
    
    def test_block_block_type(self):
        block = "1. hi\n2. hello"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "ordered_list")

    def test_divide_tag_and_children(self):
        block = "1. HI THERE\n2. HELLO\n3. holla"
        children = divide_tag_and_children(block)
        self.assertEqual(children, "HI THERE\nHELLO\nholla")

    def test_text_to_children(self):
        text = "Hello **guys**"
        children = text_to_children(text)
        self.assertEqual(children[0].tag, None)
        self.assertEqual(children[0].value, "Hello ")
        self.assertEqual(children[1].tag, "b")
        self.assertEqual(children[1].value, "guys")

    def test_block_to_html_node(self):
        block = "1. oi\n2. **hello**"
        node = block_to_html_node(block)
        self.assertEqual(node.tag, "ol")
        self.assertEqual(node.children[0].tag, "li")
        self.assertEqual(node.children[0].children[0].value, "oi")
        self.assertEqual(node.children[1].children[0].tag, "b")
        self.assertEqual(node.children[1].children[0].value, "hello")

    def test_markdown_to_hmtl_node(self):
        markdown = "# Header\n\n- 1\n- 2"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.children[0].tag, "h1")
        self.assertEqual(node.children[0].children[0].value, "Header")
        self.assertEqual(node.children[1].tag, "ul")
        self.assertEqual(node.children[1].children[0].tag, "li")
        self.assertEqual(node.children[1].children[0].children[0].value, "1")
        self.assertEqual(node.children[1].children[1].tag, "li")
        self.assertEqual(node.children[1].children[1].children[0].value, "2")

    def test_extract_title(self):
        markdown = "# Header\n\n- 1\n- 2"
        title = extract_title(markdown)
        self.assertEqual(title, "Header")

    def test_no_title(self):
        markdown = "## Header"
        with self.assertRaises(Exception):
            extract_title(markdown)

if __name__ == '__main__':
    unittest.main()