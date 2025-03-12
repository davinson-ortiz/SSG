from text_node import TextNode, TextType
from html_node import LeafNode, ParentNode
from block_markdown import markdown_to_blocks, block_to_block_type


def main():
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

    blocks = markdown_to_blocks(md)
    print(blocks)

if __name__ == "__main__":
    main()