import os
from shutil import copy, rmtree
from block_markdown import markdown_to_html_node

def to_public(from_path: str = "static", to_path: str = "public"):
    # Limpiar directorio público antes de copiar (opcional)
    if os.path.exists(to_path):
        rmtree(to_path)
    # Crear directorio destino si no existe
    os.mkdir(to_path)
    
    # Listar elementos en from_path
    for item in os.listdir(from_path):
        src_item = os.path.join(from_path, item)
        dest_item = os.path.join(to_path, item)
        
        if os.path.isfile(src_item):
            # Copiar archivo
            copy(src_item, dest_item)
            print(f"📄 Copiado {src_item} -> {dest_item}")
        else:
            # Llamada recursiva para directorios
            print(f"📂 Procesando directorio: {src_item}")
            to_public(src_item, dest_item)

def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.strip().startswith("# "):
            return line[2:]
    raise Exception("No header found")

def generate_page(from_path, template_path, to_path):
    print(f"Generating page from {from_path} to {to_path} using {template_path}")

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
    with open(to_path, "w", encoding="utf-8") as file:
        file.write(html)


def main():
    to_public()
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()