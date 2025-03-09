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


def extract_markdown_image(text: str) -> list[tuple]:
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
        images = extract_markdown_image(text)
        if not images:
            new_nodes.append(old_node)        
            continue
        
        for image in images:
            image_alt, image_link = image
            img_delimiter = f"![{image_alt}]({image_link})"
            
            # Split the text by delimiter
            sections = text.split(img_delimiter, 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":  
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            text = sections[1]
        
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        # Skip non-TEXT nodes (preserve as-is)
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        links = extract_markdown_link(text)
        if not links:
            new_nodes.append(old_node)
            continue
        
        for link in links:
            link_alt, link = link
            link_delimiter = f"[{link_alt}]({link})"
            
            # Split the text by delimiter
            sections = text.split(link_delimiter, 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_alt, TextType.LINK, link))
            text = sections[1]
        
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
    
    return new_nodes


def text_to_textnodes(text):
    # Start with a single node containing the entire text as plain text.
    nodes = [TextNode(text, TextType.TEXT)]

    # Sequentially process the nodes for images, links, code, bold, and italic.
    processing_steps = [
        (split_nodes_image, None),  # No additional args needed for images
        (split_nodes_link, None),   # No additional args needed for links
        (split_nodes_delimiter, ("`", TextType.CODE)),  # Code delimiters
        (split_nodes_delimiter, ("**", TextType.BOLD)), # Bold delimiters
        (split_nodes_delimiter, ("_", TextType.ITALIC)) # Italic delimiters
    ]

    # Apply each processing step to the nodes.
    for process_func, args in processing_steps:
        if args:
            nodes = process_func(nodes, *args)
        else:
            nodes = process_func(nodes)

    return nodes
