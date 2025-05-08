import xlsxwriter
import pandas as pd
import gym
from test.simulation.environment import BusRouteMultiAgentEnv
from stable_baselines3.common.env_util import make_vec_env
from test.training.logger import Logger

# Ajustar la carga del dataset para procesar el formato específico del archivo
DATASET_PATH = "data/route_summaries.txt"

def parse_route_summaries(file_path):
    with open(file_path, 'r') as file:
        # Ajustar el procesamiento para garantizar que las claves sean nombres de columnas
        data = []
        for line in file:
            parts = line.strip().split(', ')
            route_data = {}
            # Ajustar el procesamiento para extraer únicamente los valores relevantes
            for part in parts:
                key, value = part.split('=')
                key = key.split(':')[-1].strip()  # Extraer la clave después de ':' si existe
                route_data[key] = value.strip()
            # Agregar una columna 'route' basada en la primera parte de cada línea
            if 'route' not in route_data:
                route_data['route'] = parts[0].split(':')[0].strip()
            data.append(route_data)
        df = pd.DataFrame(data)
        df.columns = [col.strip() for col in df.columns]  # Asegurar que los nombres de columnas no tengan espacios

        # Depurar y verificar los nombres de las columnas generadas
        print("Columnas generadas:", df.columns)
        return df.apply(pd.to_numeric, errors='ignore')

dataset_df = parse_route_summaries(DATASET_PATH)

class SingleAgentWrapper(gym.Env):
    def __init__(self, env, agent_id):
        super().__init__()
        self.env = env
        self.agent_id = agent_id
        self.action_space = self.env.action_space
        self.observation_space = self.env.observation_space

    def reset(self):
        full_state = self.env.reset()
        return full_state[self.agent_id]['buses']  # Devolver un valor compatible con Gymnasium

    def step(self, action):
        full_state, rewards, dones, info = self.env.step({self.agent_id: action})
        obs = full_state[self.agent_id]['buses']  # Ajustar la observación
        reward = rewards[self.agent_id]
        done = dones.get(self.agent_id, False)  # Manejar el caso donde dones sea un diccionario
        return obs, reward, done, info

    def render(self, mode="human"):
        return self.env.render(mode=mode)

    def seed(self, seed=None):
        if hasattr(self.env, 'seed'):
            self.env.seed(seed)

def create_environment():
    # Crear un archivo Excel para guardar los resultados
    workbook = xlsxwriter.Workbook('training_results.xlsx')
    worksheet = workbook.add_worksheet()

    # Escribir encabezados en el archivo Excel
    headers = ['Iteration', 'Total Timesteps', 'FPS', 'Episode Length Mean', 'Episode Reward Mean', 'Loss', 'Value Loss', 'Policy Gradient Loss']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    # Configurar el entorno
    env = BusRouteMultiAgentEnv(route_data=dataset_df)
    single_agent_env = SingleAgentWrapper(env, agent_id=env.agents[0])
    vec_env = make_vec_env(lambda: single_agent_env, n_envs=1)

    return vec_env, Logger(workbook, worksheet), workbook, worksheet