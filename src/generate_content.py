import os
from pathlib import Path
from block_markdown import markdown_to_html_node


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Load template once to avoid repeated disk access
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
    except Exception as e:
        raise IOError(f"Error reading template file: {e}")
    
    # Process Files
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template, dest_path)
        else:
            # Create output directory for subdirectories
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(from_path, template_path, dest_path)


def generate_page(content_path, template, dest_path):
    try:
        # Read markdown content
        with open(content_path, "r", encoding="utf-8") as f:
            markdown_content = f.read()
     
        # Convert markdown to HTML
        node = markdown_to_html_node(markdown_content)
        html_content = node.to_html()
        
        # Extract title
        title = extract_title(markdown_content)
        
        # Fill template
        filled_template = (template
            .replace("{{ Title }}", title)
            .replace("{{ Content }}", html_content)
        )
        
        # Create output directory if it doesn't exist
        dest_dir_path = os.path.dirname(dest_path)
        if dest_dir_path != "":
            os.makedirs(dest_dir_path, exist_ok=True)
        
        # Write output file
        with open(dest_path, "w", encoding="utf-8") as f:
            f.write(filled_template)
            
        print(f"Generated: {content_path} -> {dest_path}")
        return True
    except Exception as e:
        print(f"Error generating {content_path}: {e}")
        return False

        
        
def extract_title(markdown: str) -> str:
    """
    Extract title from markdown content.
    
    Args:
        markdown: Markdown content
        
    Returns:
        Title string
        
    Raises:
        ValueError: If no title is found
    """
    lines = markdown.split("\n")
    for line in lines:
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No title found in markdown content")
