from enum import Enum
from htmlnode import LeafNode
import re


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url
        
    def __eq__(self, value: TextType) -> bool:
        if not isinstance(value, TextNode):
            return False
        return (self.text == value.text and
                self.text_type == value.text_type and
                self.url == value.url)
        
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
  
    
def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"invalid text type: {text_node.text_type}")


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        # Skip non-TEXT nodes (preserve as-is)
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        # Split the text by delimiter
        sections = old_node.text.split(delimiter)
        # Check for balanced delimiters (odd number of sections means balanced)
        if len(sections) % 2 == 0:
            raise SyntaxError(f"Invalid markdown: opening delimiter '{delimiter}' without matching closing delimiter")
        # Process each section, keeping track of its type based on position
        for i, text in enumerate(sections):
            # Skip empty sections only if they're regular text (optional, based on requirements)
            if text == "" and i % 2 == 0:
                continue
            # Determine the appropriate text type based on position
            section_type = text_type if i % 2 == 1 else TextType.TEXT
            # Add to result list
            new_nodes.append(TextNode(text, section_type))
       
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text) or re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        # Skip non-TEXT nodes (preserve as-is)
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        for image in extract_markdown_images(text):
            image_alt, image_link = image
            img_delimiter = f"![{image_alt}]({image_link})"
            # Split the text by delimiter
            sections = text.split(img_delimiter, 1)
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            text = sections[-1]
       
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        # Skip non-TEXT nodes (preserve as-is)
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        for link in extract_markdown_images(text):
            link_alt, link = link
            link_delimiter = f"[{link_alt}]({link})"
            # Split the text by delimiter
            sections = text.split(link_delimiter, 1)
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_alt, TextType.LINK, link))
            text = sections[-1]
       
    return new_nodes