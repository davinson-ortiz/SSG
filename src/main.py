import os
from shutil import copy, rmtree
from block_markdown import markdown_to_html_node

def to_public(src_path: str = "static", dest_path: str = "public"):
    # Limpiar directorio público antes de copiar (opcional)
    if os.path.exists(dest_path):
        rmtree(dest_path)
    # Crear directorio destino si no existe
    os.mkdir(dest_path)
    
    # Listar elementos en src_path
    for item in os.listdir(src_path):
        src_item = os.path.join(src_path, item)
        dest_item = os.path.join(dest_path, item)
        
        if os.path.isfile(src_item):
            # Copiar archivo
            copy(src_item, dest_item)
        else:
            # Llamada recursiva para directorios
            to_public(src_item, dest_item)

def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.strip().startswith("# "):
            return line[2:]
    raise Exception("No header found")

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
    html = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    # Write the html file to des_path
    with open(dest_path, "w", encoding="utf-8") as file:
        file.write(html)


def main():
    to_public()
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()