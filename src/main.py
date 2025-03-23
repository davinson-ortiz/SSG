import os
from shutil import rmtree
from copy_static import copy_files_recursive
from generate_content import generate_pages_recursive


dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    # Limpiar directorio público antes de copiar (opcional)
    if os.path.exists(dir_path_public):
        rmtree(dir_path_public)
    
    copy_files_recursive(dir_path_static, dir_path_public)
    
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)


if __name__ == "__main__":
    main()