import os
from block_markdown import markdown_to_html_node


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    pages = md_files_paths(dir_path_content)
    for page in pages:
        dest_dir_path = page.replace("./content", dest_dir_path).replace("index.md", "index.html")
        generate_page(page, template_path, dest_dir_path)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as content:
        md = content.read()
    with open(template_path, "r", encoding="utf-8") as content:
        template = content.read()
    
    node = markdown_to_html_node(md)
    html = node.to_html()
    
    title = extract_title(md)
    # Replace placeholders
    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    # Write the html file to des_path
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    
    with open(dest_path, "w", encoding="utf-8") as file:
        file.write(full_html)
        
        
def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.strip().startswith("# "):
            return line[2:]
    raise Exception("No header found")


def md_files_paths(source_dir_path: str) -> list[str]:
    paths = []
    # Listar elementos en from_path
    for filename in os.listdir(source_dir_path):
        path = os.path.join(source_dir_path, filename)
        if os.path.isfile(path):
            # Add path
            paths.append(path)
        else:
            paths.extend(md_files_paths(path))
    return paths


generate_pages_recursive("./content", "./template.html", "./public")