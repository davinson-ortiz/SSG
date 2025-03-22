from enum import Enum
import re
from html_node import HTMLNode, ParentNode
from text_node import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

# Precompile patterns as constants; compile patterns only once
PATTERNS = {
    re.compile(r"^#{1,6}\s.+"): BlockType.HEADING,
    re.compile(r"^>\s[^\s].+"): BlockType.QUOTE,
    re.compile(r"^-\s[^\s].+"): BlockType.UNORDERED_LIST,
    re.compile(r"^\d+\.\s[^\s].+"): BlockType.ORDERED_LIST,
}

def block_to_block_type(md_block: str) -> BlockType: 
    """Determine the block type of a given Markdown block."""
    # Special case for code blocks
    if md_block.startswith("```") and md_block.endswith("```"):
        return BlockType.CODE
    
    # Check first line against patterns
    first_line = md_block.split('\n', 1)[0]

    for pattern, block_type in PATTERNS.items():
        if pattern.match(first_line):
            return block_type
    
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown: str) -> list[str]:
    """
    Parses a Markdown document into a list of block elements.
    
    Returns a list instead of a generator.
    """
    parsed_blocks = []  # Store parsed blocks
    temp_block = []   # Temporarily store lines of the current block
    inside_code_block = False

    for line in markdown.split("\n"):
        # Handle code blocks
        if line.startswith("```"):  
            inside_code_block = not inside_code_block  # Toggle code block state
            temp_block.append(line)
            if not inside_code_block:  # If code block just ended, store it
                parsed_blocks.append("\n".join(temp_block))
                temp_block = []
            continue

        if inside_code_block:
            temp_block.append(line)
            continue

        # If we hit an empty line and there's something in the block, save it
        if not line.strip():
            if temp_block:
                parsed_blocks.append("\n".join(temp_block))
                temp_block = []
            continue
        
        #If not code blocks or empty lies, just append the line.
        temp_block.append(line)

    if temp_block:  # Store any remaining block
        parsed_blocks.append("\n".join(temp_block))

    return parsed_blocks


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block: str) -> ParentNode:
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return ulist_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return olist_to_html_node(block)
        case _:
            raise ValueError(f"Unknown block type: {block_type}")


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block: str) -> ParentNode:
    # Headings are wrapped in <h1> to <h6> tags based on the number of #
    heading_level = block.count("#", 0, 7)
    text = block[heading_level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{heading_level}", children)


def code_to_html_node(block):
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
