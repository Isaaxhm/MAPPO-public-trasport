# Instrucciones para integrar ResultadosEncuestas.csv en el modelo MAPPO

## 1. Procesamiento de ResultadosEncuestas.csv
- Leer el archivo `data/ResultadosEncuestas.csv` usando pandas.
- Agrupar los datos por `route_id` y calcular la satisfacción promedio, el sentimiento promedio (puede mapearse a valores numéricos), y otros indicadores relevantes (por ejemplo, tiempo de espera promedio).
- Generar un diccionario o DataFrame con estos valores agregados por ruta.

## 2. Integración en el entorno multiagente
- Modificar el entorno multiagente (`BusRouteMultiAgentEnv` o el que corresponda) para que reciba los datos procesados de las encuestas.
- Al calcular la recompensa de cada agente (ruta), utilizar la satisfacción promedio y/o el sentimiento de los usuarios de esa ruta como parte de la función de recompensa.
- Ejemplo de función de recompensa:
  ```python
  def calculate_rewards(state, survey_stats):
      rewards = {}
      for route_id, info in state.items():
          satisfaction = survey_stats.get(route_id, {}).get('satisfaction', 0)
          # Puedes combinar satisfacción, tiempo de espera, etc.
          rewards[route_id] = satisfaction  # O una fórmula más compleja
      return rewards
  ```

## 3. Flujo sugerido
1. Procesar encuestas al inicio del entrenamiento y pasar los resultados al entorno.
2. En cada paso del entorno, usar los datos agregados de encuestas para calcular la recompensa de cada agente.

## 4. Ejemplo de procesamiento de encuestas
```python
import pandas as pd

def process_survey_results(path):
    df = pd.read_csv(path)
    # Mapear sentimiento a valor numérico
    df['sentiment_num'] = df['sentiment'].map({'Positivo': 1, 'Negativo': -1})
    grouped = df.groupby('route_id').agg({
        'satisfaction': 'mean',
        'wait_time_rating': 'mean',
        'sentiment_num': 'mean'
    }).reset_index()
    survey_stats = grouped.set_index('route_id').to_dict(orient='index')
    return survey_stats
```

## 5. Modificación del entorno
- Asegúrate de que el entorno reciba `survey_stats` y lo use en la función de recompensa.
- Si usas `calculate_rewards`, pásale también `survey_stats`.

---
Estas instrucciones permiten que el modelo MAPPO utilice la información de las encuestas para aprender políticas que maximicen la satisfacción de los usuarios.
