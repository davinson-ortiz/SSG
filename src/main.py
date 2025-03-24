import os
import sys
from shutil import rmtree
from copy_static import copy_files_recursive
from generate_content import generate_pages_recursive


dir_path_static = "./static"
# dir_path_public = "./public"
dir_path_docs = "./docs" # For github pages!!!
dir_path_content = "./content"
template_path = "./template.html"

def main():
    if len(sys.argv) == 2:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    print("basepath: ", basepath)
    # Limpiar directorio público antes de copiar (opcional)
    if os.path.exists(dir_path_docs):
        rmtree(dir_path_docs)
    
    copy_files_recursive(dir_path_static, dir_path_docs)
    generate_pages_recursive(dir_path_content, template_path, dir_path_docs, basepath)


if __name__ == "__main__":
    main()