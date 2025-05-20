---
applyTo: '**'
---
# Proyecto MAPPO para el MICAI 2025
Este proyecto se centra en la parte de una implementacion de un modelo MAPPO (Multi-Agent Proximal Policy Optimization) para el MICAI 2025. El objetivo de entre parte del proyecto es crear un modelo que pueda utilizar los dos siguientes archivos:
- `gtfs`: El cual contiene datos de GTFS (General Transit Feed Specification) que describen rutas, paradas y horarios de transporte público.
- `ResultadosEncuestas.csv`: El cual contiene datos de encuestas realizadas a usuarios del transporte público, incluyendo información sobre su experiencia, preferencias y sugerencias.
- `route_summaries.txt`: El cual contiene resúmenes de rutas, incluyendo información sobre la duración, distancia y otros parámetros relevantes. Este archivo es un resumen de los datos de GTFS y se utiliza para entrenar el modelo MAPPO. 

## Acciones del Proyecto
Los objetivos que son prioridades para el proyecto son:
- Quiero que analices el archivo ResultadosEncuestas.csv y me digas como se crear un modelo MAPPO para el MICAI 2025.

# Cambios para migrar la funcionalidad de test/ a src/ y agregar un lanzador interactivo

## 1. Migración de carpetas y archivos
- Mueve el contenido de `test/` a `src/` manteniendo la estructura de subcarpetas (`agents/`, `env/`, etc.).
- Elimina la carpeta `test/` después de la migración.

## 2. Lanzador interactivo
- Crea un archivo en `src/🚌_launcher.py` que:
  - Verifica la existencia de los archivos y carpetas requeridos: `gtfs/`, `ResultadosEncuestas.csv`, `route_summaries.txt`.
  - Si falta alguno, pregunta al usuario si desea intentar conseguirlo. Si no se consigue, termina la ejecución.
  - Si todo está presente, pregunta si desea transformar los datos y crear el modelo MAPPO.
  - Si el usuario acepta, ejecuta el pipeline de procesamiento y entrenamiento.

## 3. Cambios en el flujo de ejecución
- El usuario debe ejecutar el lanzador `🚌_launcher.py` para iniciar el proceso.
- El lanzador guía al usuario paso a paso y asegura que los archivos requeridos estén presentes antes de continuar.

## 4. Recomendaciones
- Asegúrate de que los imports en los scripts migrados apunten a la nueva ubicación en `src/`.
- Actualiza cualquier referencia a rutas de archivos si es necesario.

---
Con estos cambios, el flujo es más robusto y amigable para el usuario, asegurando la disponibilidad de los datos antes de procesar o entrenar el modelo MAPPO.
