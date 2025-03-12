import unittest
from block_markdown import markdown_to_blocks, BlockType, block_to_block_type

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


class TestBlockTypeDetection(unittest.TestCase):

    def test_paragraphs(self):
        # Simple paragraph
        self.assertEqual(
            block_to_block_type("This is a simple paragraph."),
            BlockType.PARAGRAPH
        )
        
        # Multi-line paragraph
        self.assertEqual(
            block_to_block_type("This is a paragraph\nthat spans multiple lines\nwith different content."),
            BlockType.PARAGRAPH
        )
        
        # Paragraph with markdown-like content that isn't at start of line
        self.assertEqual(
            block_to_block_type("This contains a # that looks like a heading"),
            BlockType.PARAGRAPH
        )
        
        # Empty or whitespace-only content
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("   "), BlockType.PARAGRAPH)
        
    def test_headings(self):
        # Simple heading levels 1-6
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### Heading 4"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### Heading 5"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        
        # Heading with additional content
        self.assertEqual(
            block_to_block_type("# Heading with *markdown* formatting"),
            BlockType.HEADING
        )
        
        # Multi-line heading (only first line matters)
        self.assertEqual(
            block_to_block_type("# Heading\nWith following content"),
            BlockType.HEADING
        )
        
        # Invalid heading (too many #'s)
        self.assertEqual(block_to_block_type("####### Not a heading"), BlockType.PARAGRAPH)
        
        # Invalid heading (missing space)
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)
        
    def test_code_blocks(self):
        # Simple code block
        self.assertEqual(
            block_to_block_type("```\ncode block\n```"),
            BlockType.CODE
        )
        
        # Code block with language
        self.assertEqual(
            block_to_block_type("```python\ndef hello():\n    print('Hello')\n```"),
            BlockType.CODE
        )
        
        # Code block with content that looks like other block types
        self.assertEqual(
            block_to_block_type("```\n# Not a heading\n- Not a list\n> Not a quote\n```"),
            BlockType.CODE
        )
        
        # Incomplete code block (missing end marker)
        self.assertEqual(
            block_to_block_type("```\nIncomplete code block"),
            BlockType.PARAGRAPH
        )
        
    def test_quotes(self):
        # Simple quote
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        
        # Multi-line quote
        self.assertEqual(
            block_to_block_type("> This is a quote\n> that continues"),
            BlockType.QUOTE
        )
        
        # Quote with markdown-like content
        self.assertEqual(
            block_to_block_type("> # Heading inside a quote"),
            BlockType.QUOTE
        )
        
        # Invalid quote (missing space)
        self.assertEqual(block_to_block_type(">No space"), BlockType.PARAGRAPH)
        
    def test_unordered_lists(self):
        # Simple unordered list item
        self.assertEqual(block_to_block_type("- List item"), BlockType.UNORDERED_LIST)
        
        # Multi-line list item
        self.assertEqual(
            block_to_block_type("- List item\n  with continuation"),
            BlockType.UNORDERED_LIST
        )
        
        # List with markdown-like content
        self.assertEqual(
            block_to_block_type("- # Not a heading inside list"),
            BlockType.UNORDERED_LIST
        )
        
        # Invalid list item (missing space)
        self.assertEqual(block_to_block_type("-No space"), BlockType.PARAGRAPH)
        
    def test_ordered_lists(self):
        # Simple ordered list items with different numbers
        self.assertEqual(block_to_block_type("1. List item"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("42. List item"), BlockType.ORDERED_LIST)
        
        # Multi-line ordered list item
        self.assertEqual(
            block_to_block_type("1. List item\n   with continuation"),
            BlockType.ORDERED_LIST
        )
        
        # Ordered list with markdown-like content
        self.assertEqual(
            block_to_block_type("1. # Not a heading inside list"),
            BlockType.ORDERED_LIST
        )
        
        # Invalid ordered list (missing space)
        self.assertEqual(block_to_block_type("1.No space"), BlockType.PARAGRAPH)
        
        # Invalid ordered list (extra space)
        self.assertEqual(block_to_block_type("1.  Two spaces"), BlockType.PARAGRAPH)
        
    def test_edge_cases(self):
        # Mixed blocks (should detect based on first line)
        self.assertEqual(
            block_to_block_type("# Heading\n- List item\n> Quote"),
            BlockType.HEADING
        )
        
        # Indented content
        self.assertEqual(block_to_block_type("  Regular paragraph with indent"), BlockType.PARAGRAPH)
        #self.assertEqual(block_to_block_type("  # Still a heading"), BlockType.HEADING)
        
        # Leading/trailing whitespace
        #self.assertEqual(block_to_block_type("  # Heading with whitespace  "), BlockType.HEADING)
        
        # Code fence not at start of string
        self.assertEqual(
            block_to_block_type("Some text\n```\ncode\n```"),
            BlockType.PARAGRAPH
        )
        
        # Nested markdown should be detected based on outer level
        self.assertEqual(
            block_to_block_type("- Outer list item with ```code``` block inside"),
            BlockType.UNORDERED_LIST
        )


if __name__ == "__main__":
    unittest.main()