import unittest
from block_markdown import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    
    def test_basic_blocks(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        ]
        
        self.assertEqual(markdown_to_blocks(markdown), expected)
    
    def test_empty_blocks(self):
        markdown = """# First block


Second block



Third block"""
        
        expected = [
            "# First block",
            "Second block",
            "Third block"
        ]
        
        self.assertEqual(markdown_to_blocks(markdown), expected)
    
    def test_blocks_with_internal_newlines(self):
        markdown = """# Heading

Paragraph with
multiple
lines.

- List item 1
- List item 2"""
        
        expected = [
            "# Heading",
            "Paragraph with\nmultiple\nlines.",
            "- List item 1\n- List item 2"
        ]
        
        self.assertEqual(markdown_to_blocks(markdown), expected)
    
    def test_empty_input(self):
        markdown = ""
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)
    
    def test_only_whitespace(self):
        markdown = "   \n\n  \t  \n\n   "
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

if __name__ == "__main__":
    unittest.main()