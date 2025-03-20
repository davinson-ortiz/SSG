import unittest
from html_node import HTMLNode, ParentNode
from block_markdown import (
    markdown_to_blocks, 
    BlockType, 
    block_to_block_type,
    markdown_to_html_node, 
    block_to_html_node, 
    text_to_children,
    paragraph_to_html_node,
    code_to_html_node,
    ulist_to_html_node,
    olist_to_html_node,
    quote_to_html_node,
    heading_to_html_node
)


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


class TestMarkdownToHTML(unittest.TestCase):

    def test_markdown_to_html_node(self):
        markdown = "# Heading\n\nSome paragraph\n\n- List item"
        html_node = markdown_to_html_node(markdown)
        self.assertIsInstance(html_node, ParentNode)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 3)

    def test_block_to_html_node_paragraph(self):
        block = "This is a paragraph."
        html_node = block_to_html_node(block)
        self.assertIsInstance(html_node, ParentNode)
        self.assertEqual(html_node.tag, "p")

    def test_block_to_html_node_heading(self):
        block = "### Heading 3"
        html_node = block_to_html_node(block)
        self.assertIsInstance(html_node, ParentNode)
        self.assertEqual(html_node.tag, "h3")

    def test_block_to_html_node_code(self):
        block = "```\ncode block\n```"
        html_node = block_to_html_node(block)
        self.assertIsInstance(html_node, ParentNode)
        self.assertEqual(html_node.tag, "pre")
        self.assertEqual(html_node.children[0].tag, "code")

    def test_block_to_html_node_quote(self):
        block = "> Quote line 1\n> Quote line 2"
        html_node = block_to_html_node(block)
        self.assertIsInstance(html_node, ParentNode)
        self.assertEqual(html_node.tag, "blockquote")

    def test_block_to_html_node_unordered_list(self):
        block = "- Item 1\n- Item 2"
        html_node = block_to_html_node(block)
        self.assertIsInstance(html_node, ParentNode)
        self.assertEqual(html_node.tag, "ul")
        self.assertEqual(len(html_node.children), 2)

    def test_block_to_html_node_ordered_list(self):
        block = "1. Item 1\n2. Item 2"
        html_node = block_to_html_node(block)
        self.assertIsInstance(html_node, ParentNode)
        self.assertEqual(html_node.tag, "ol")
        self.assertEqual(len(html_node.children), 2)

    def test_text_to_children(self):
        text = "This is **bold** and *italic* text."
        children = text_to_children(text)
        self.assertIsInstance(children, list)
        self.assertTrue(all(isinstance(child, HTMLNode) for child in children))

    def test_paragraph_to_html_node(self):
        block = "This is a paragraph."
        html_node = paragraph_to_html_node(block)
        self.assertIsInstance(html_node, ParentNode)
        self.assertEqual(html_node.tag, "p")

    def test_heading_to_html_node(self):
        block = "## Heading 2"
        html_node = heading_to_html_node(block)
        self.assertIsInstance(html_node, ParentNode)
        self.assertEqual(html_node.tag, "h2")

    def test_code_to_html_node(self):
        block = "```\ncode block\n```"
        html_node = code_to_html_node(block)
        self.assertIsInstance(html_node, ParentNode)
        self.assertEqual(html_node.tag, "pre")
        self.assertEqual(html_node.children[0].tag, "code")

    def test_olist_to_html_node(self):
        block = "1. First item\n2. Second item"
        html_node = olist_to_html_node(block)
        self.assertIsInstance(html_node, ParentNode)
        self.assertEqual(html_node.tag, "ol")
        self.assertEqual(len(html_node.children), 2)

    def test_ulist_to_html_node(self):
        block = "- First item\n- Second item"
        html_node = ulist_to_html_node(block)
        self.assertIsInstance(html_node, ParentNode)
        self.assertEqual(html_node.tag, "ul")
        self.assertEqual(len(html_node.children), 2)

    def test_quote_to_html_node(self):
        block = "> Quote line 1\n> Quote line 2"
        html_node = quote_to_html_node(block)
        self.assertIsInstance(html_node, ParentNode)
        self.assertEqual(html_node.tag, "blockquote")

    def test_quote_to_html_node_invalid(self):
        block = "> Valid line\nInvalid line"
        with self.assertRaises(ValueError):
            quote_to_html_node(block)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()