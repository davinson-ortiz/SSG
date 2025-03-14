from text_node import TextNode, TextType
from html_node import LeafNode, ParentNode, HTMLNode
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType


def main():
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

    blocks = markdown_to_blocks(md)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.QUOTE:
                html_nodes.append(HTMLNode("<blockquote>", block))
            case BlockType.UNORDERED_LIST:
                html_nodes.append(HTMLNode("<ul>", block))
            case BlockType.ORDERED_LIST:
                html_nodes.append(HTMLNode("<ol>", block))
            case BlockType.CODE:
                html_nodes.append(HTMLNode("<pre><code>", block))
            case BlockType.HEADING:
                html_nodes.append(HTMLNode("<h1>", block))
            case BlockType.PARAGRAPH:
                html_nodes.append(HTMLNode("<p>", block))
    
    return html_nodes


def text_to_children(text):
    for html

if __name__ == "__main__":
    main()