from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(md_block): 
    # Compile patterns only once (would be better as constants outside function)
    patterns = [
        (re.compile(r"^#{1,6}\s.+"), BlockType.HEADING),
        (re.compile(r"^>\s[^\s].+"), BlockType.QUOTE),
        (re.compile(r"^-\s[^\s].+"), BlockType.UNORDERED_LIST),
        (re.compile(r"^\d+\.\s[^\s].+"), BlockType.ORDERED_LIST)
    ]
    
    # Special case for code blocks
    if md_block.startswith("```") and md_block.endswith("```"):
        return BlockType.CODE
    
    # Check first line against patterns
    first_line = md_block.split('\n')[0] if '\n' in md_block else md_block
    for pattern, block_type in patterns:
        if pattern.match(first_line):
            return block_type
    
    return BlockType.PARAGRAPH



def markdown_to_blocks(markdown: str)->list[str]:
    return [block.strip() for block in markdown.split("\n\n") if block.strip()]
