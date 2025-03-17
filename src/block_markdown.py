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
    blocks = []  # Store parsed blocks
    block = []   # Temporarily store lines of the current block
    inside_code_block = False

    for line in markdown.split("\n"):
        # Handle code blocks
        if line.startswith("```"):  
            inside_code_block = not inside_code_block  # Toggle code block state
            block.append(line)
            if not inside_code_block:  # If code block just ended, store it
                blocks.append("\n".join(block))
                block = []
            continue

        if inside_code_block:
            block.append(line)
            continue

        # If we hit an empty line and there's something in the block, save it
        if not line.strip():
            if block:
                blocks.append("\n".join(block))
                block = []
            continue
        
        #If not code blocks or empty lies, just append the line.
        block.append(line)

    if block:  # Store any remaining block
        blocks.append("\n".join(block))

    return blocks


def markdown_to_html_node(markdown):
    block_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                # Paragraphs are wrapped in <p> tags
                block_nodes.append(HTMLNode("p", block))
            case BlockType.HEADING:
                # Headings are wrapped in <h1> to <h6> tags based on the number of #
                heading_level = block.count("#")
                if heading_level < 1 or heading_level > 6:
                    raise ValueError(f"Invalid heading level: {heading_level}")
                block_nodes.append(HTMLNode(f"h{heading_level}", block.lstrip("# ")))
            case BlockType.CODE:
                # Code blocks are wrapped in <pre><code> tags
                code_content = block.strip("```").strip()  # Remove Markdown code block delimiters
                code_node = HTMLNode("code", code_content)
                block_nodes.append(HTMLNode("pre", code_node))
            case BlockType.QUOTE:
                # Quote blocks are wrapped in <blockquote> tags
                block_nodes.append(HTMLNode("blockquote", block.lstrip("> ")))
            case BlockType.UNORDERED_LIST:
                # Unordered lists are wrapped in <ul> tags, with each item in <li> tags
                list_items = block.split("\n")
                li_nodes = [HTMLNode("li", item.lstrip("- ")) for item in list_items]
                block_nodes.append(HTMLNode("ul", li_nodes))
            case BlockType.ORDERED_LIST:
                # Ordered lists are wrapped in <ol> tags, with each item in <li> tags
                list_items = block.split("\n")
                li_nodes = [HTMLNode("li", item.split(". ", 1)[1]) for item in list_items]
                block_nodes.append(HTMLNode("ol", li_nodes))
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


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
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
