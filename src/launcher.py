import os
import sys
import questionary
import time
from main import process_csv

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data')
GTFS_PATH = os.path.join(DATA_PATH, 'gtfs')
SURVEY_PATH = os.path.join(DATA_PATH, 'ResultadosEncuestas.csv')
ROUTES_PATH = os.path.join(DATA_PATH, 'route_summaries.txt')

def check_files():
    missing = []
    if not os.path.exists(GTFS_PATH) or not os.listdir(GTFS_PATH):
        missing.append('gtfs')
    if not os.path.exists(SURVEY_PATH):
        missing.append('ResultadosEncuestas.csv')
    if not os.path.exists(ROUTES_PATH):
        missing.append('route_summaries.txt')
    return missing

def try_download(file_name):
    print(f"No se encontró {file_name}. Debe obtenerlo manualmente.")
    return False

def main():
    print("Bienvenido al entorno de entrenamiento MAPPO para MICAI 2025.")
    time.sleep(1)
    missing = check_files()
    for file in missing:
        answer = questionary.confirm(f"¿Desea intentar conseguir el archivo '{file}' automáticamente?").ask()
        if answer:
            print(f"Intentando conseguir '{file}'...")
            time.sleep(1)
            if not try_download(file):
                print(f"No se pudo conseguir '{file}'. Terminando ejecución.")
                sys.exit(1)
        else:
            print(f"No se puede continuar sin '{file}'. Terminando ejecución.")
            sys.exit(1)
    print("\nTodos los archivos requeridos están presentes.")
    time.sleep(1)
    answer = questionary.confirm("¿Desea transformar los datos GTFS y crear el modelo MAPPO?").ask()
    if answer:
        print("\nIniciando procesamiento de datos GTFS...")
        time.sleep(1)
        print("Cargando datos GTFS...")
        time.sleep(1)
        print("Procesando rutas...")
        time.sleep(1)
        print("Generando route_summaries.txt...")
        time.sleep(1)
        process_csv()
        print("\nTransformación y análisis completados. ¡Listo para entrenar el modelo!")
    else:
        print("Ejecución finalizada por el usuario.")

if __name__ == "__main__":
    main()
