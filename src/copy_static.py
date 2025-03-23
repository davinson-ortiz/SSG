import os
from shutil import copy


def copy_files_recursive(source_dir_path, dest_dir_path):
    # Crear directorio destino si no existe
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    
    # Listar elementos en from_path
    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        
        if os.path.isfile(from_path):
            # Copiar archivo
            copy(from_path, dest_path)
            print(f"📄 Copiado {from_path} -> {dest_path}")
        else:
            # Llamada recursiva para directorios
            print(f"📂 Procesando directorio: {from_path}")
            copy_files_recursive(from_path, dest_path)
