from text_node import TextNode, TextType
import re


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
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    

def extract_markdown_link(text:str)-> list[tuple]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


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
        for link in extract_markdown_link(text):
            link_alt, link = link
            link_delimiter = f"[{link_alt}]({link})"
            # Split the text by delimiter
            sections = text.split(link_delimiter, 1)
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_alt, TextType.LINK, link))
            text = sections[-1]
       
    return new_nodes
