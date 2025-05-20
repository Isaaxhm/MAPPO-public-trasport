import os
import shutil

def file_if_exist(src_files, dest_dir):
    """
    Copia archivos de src_files a dest_dir si existen.
    """
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    for file_path in src_files:
        if os.path.isfile(file_path):
            shutil.copy(file_path, dest_dir)
            print(f"Archivo copiado: {file_path}")
        else:
            print(f"Archivo no encontrado: {file_path}")

    # Ejemplo de uso:
    # archivos = ["data/gtfs/CDMX/routes.txt", "data/gtfs/CDMX/stops.txt"]
    # destino = "data/backup"
    # copy_files_if_exist(archivos, destino)