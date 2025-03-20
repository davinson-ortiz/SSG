import os
from shutil import copy, rmtree

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
            print(f"📄 Copiado {src_item} -> {dest_item}")
        else:
            # Llamada recursiva para directorios
            print(f"📂 Procesando directorio: {src_item}")
            to_public(src_item, dest_item)

def main():
    print("📂 Procesando directorio: static")
    to_public()

if __name__ == "__main__":
    main()