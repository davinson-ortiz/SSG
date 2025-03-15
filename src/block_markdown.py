from enum import Enum
import re
from typing import Iterator

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
def block_to_block_type(md_block): 
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
