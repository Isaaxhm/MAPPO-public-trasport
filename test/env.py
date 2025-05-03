import gymnasium as gym
from gymnasium import spaces
import numpy as np

class TransitRoutesEnv(gym.Env):
    """Entorno multi-agente con rutas de transporte como agentes."""
    metadata = {"render.modes": ["human"]}

    def __init__(self, route_data):
        super().__init__()
        # route_data: dict route_id -> [buses, headway, speed, demand]
        self.route_ids = list(route_data.keys())
        self.route_data = route_data
        self.num_agents = len(self.route_ids)

        # Observación: vector de 4 floats por agente
        self.observation_space = spaces.Box(0, np.inf, shape=(4,), dtype=np.float32)
        # Acción: discreta ajuste de buses de -5 a +5
        self.action_space = spaces.Discrete(11)

    def reset(self):
        # Estado inicial: obs por ruta
        obs = {rid: np.array(self.route_data[rid], dtype=np.float32)
               for rid in self.route_ids}
        return obs, {}

    def step(self, action_dict):
        obs, rewards, dones, infos = {}, {}, {}, {}
        # Para cada agente, la acción es un entero 0-10; mapeamos a delta buses
        for rid, action in action_dict.items():
            delta = action - 5  # [-5..+5]
            data = self.route_data[rid]
            # Actualizar número de buses y recalcular headway
            buses = max(1, data[0] + delta)
            headway = (data[0] * data[1]) / buses
            speed, demand = data[2], data[3]
            self.route_data[rid] = [buses, headway, speed, demand]

            # Definir recompensa operativa: invertimos headway y multiplicamos por demanda
            rewards[rid] = (demand / headway)
            obs[rid] = np.array(self.route_data[rid], dtype=np.float32)
            dones[rid] = False
            infos[rid] = {}

        # Episodio termina después de un paso
        dones['__all__'] = True
        return obs, rewards, dones, infos

    def render(self, mode='human'):
        print(self.route_data)