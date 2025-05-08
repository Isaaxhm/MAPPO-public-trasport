import pandas as pd
import gymnasium as gym
from gymnasium.spaces import Box, Discrete # Used for defining observation/action spaces
import pettingzoo # A common library for multi-agent environments
from pettingzoo.utils import parallel_to_aec, aec_to_parallel # Utilities
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
import numpy as np

# --- 1. Load the data (Used potentially for initializing the environment) ---
file_path = 'data/route_summaries.txt'
try:
    # The data format seems non-standard for direct CSV parsing.
    # We'll parse it manually or adjust based on the actual file structure.
    # Assuming each line is a record and you need to extract values.
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            if line.strip() and line.startswith("Route"):
                parts = line.strip().split(': ')
                route_name = parts[0].split(' ')[1]
                metrics_str = parts[1]
                metrics = {}
                for item in metrics_str.split(', '):
                    key, value = item.split('=')
                    key = key.strip()  # Eliminar espacios adicionales
                    value = value.strip().replace('min', '')  # Eliminar 'min' y espacios
                    metrics[key] = float(value)
                data.append({'route': route_name, **metrics})

    dataset_df = pd.DataFrame(data)
    print("Data loaded successfully (or parsed manually):")
    print(dataset_df.head())

except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
    # Handle error or exit
    exit()
except Exception as e:
    print(f"Error loading or parsing data: {e}")
    # Handle error or exit
    exit()


# --- 2. Define the Multi-Agent Environment (Conceptual - YOU NEED TO IMPLEMENT THIS) ---
# This is the MOST IMPORTANT part that is MISSING and cannot be built from the CSV alone.
# This is just a placeholder class structure.
class BusRouteMultiAgentEnv(pettingzoo.ParallelEnv):
    def __init__(self, route_data):
        super().__init__()
        self.route_data = route_data
        self.routes = route_data['route'].tolist()
        self.possible_agents = self.routes # Each route is an agent

        # Define observation and action spaces for each agent
        # These are examples - you need to design them based on your problem
        self._observation_spaces = {
            agent: Box(low=-float('inf'), high=float('inf'), shape=(4,), dtype=float) # Example: [buses, headway, speed, demand] or scaled/normalized
            for agent in self.possible_agents
        }
        # Example Action Space: Discrete actions like [Increase Speed, Decrease Speed, Maintain Speed]
        # Or a continuous action space depending on what agents can control.
        self._action_spaces = {
             agent: Discrete(3) # Example: 3 discrete actions per agent
             for agent in self.possible_agents
        }

        self.agents = self.possible_agents[:]
        self.state = None # This would hold the dynamic state of the environment
        self.timestep = 0

    def observation_space(self, agent):
        return self._observation_spaces[agent]

    def action_space(self, agent):
        return self._action_spaces[agent]

    def reset(self, seed=None, options=None):
        self.agents = self.possible_agents[:]
        self.timestep = 0
        self.state = self._initialize_state()
        observations = self._get_observations()
        infos = {agent: {} for agent in self.agents}
        return observations, infos

    def step(self, actions):
        self.timestep += 1

        # Apply the actions from all agents to the environment
        # Update the environment state based on actions and dynamics
        self._apply_actions_and_update_state(actions)

        # Calculate rewards for each agent
        rewards = self._calculate_rewards()

        # Determine if the episode is finished
        terminations = {agent: False for agent in self.agents}
        truncations = {agent: False for agent in self.agents}
        if self.timestep >= 1000: # Example: End after 1000 steps
             truncations = {agent: True for agent in self.agents}

        # Get observations for the next state
        observations = self._get_observations()

        infos = {agent: {} for agent in self.agents}

        return observations, rewards, terminations, truncations, infos

    # --- Placeholder methods you MUST implement ---
    def _initialize_state(self):
        state = {}
        for _, row in self.route_data.iterrows():
            route_name = row['route']
            state[route_name] = {
                'buses': row['buses'],
                'headway': row['headway'],
                'speed': row['speed'],
                'demand': row['demand'],
            }
        return state

    def _apply_actions_and_update_state(self, actions):
        for agent, action in actions.items():
            if action == 0:  # Disminuir velocidad
                self.state[agent]['speed'] = max(0, self.state[agent]['speed'] - 0.01)
            elif action == 1:  # Mantener velocidad
                pass
            elif action == 2:  # Aumentar velocidad
                self.state[agent]['speed'] += 0.01

            # Actualizar headway y demanda basados en la nueva velocidad
            self.state[agent]['headway'] = max(1, self.state[agent]['headway'] - self.state[agent]['speed'] * 0.1)
            self.state[agent]['demand'] = max(0, self.state[agent]['demand'] - self.state[agent]['speed'] * 0.05)

    def _calculate_rewards(self):
        rewards = {}
        for agent, data in self.state.items():
            # Penalizar headway alto y recompensar velocidad eficiente
            rewards[agent] = -data['headway'] + data['speed'] * 0.5
        return rewards

    def _get_observations(self):
        observations = {}
        for agent in self.agents:
            obs_data = self.state[agent]
            observations[agent] = np.array([
                obs_data['buses'],
                obs_data['headway'],
                obs_data['speed'],
                obs_data['demand'],
            ], dtype=np.float32)
        return observations

    def render(self):
        # Optional: Implement rendering for visualization
        pass

    def close(self):
        # Optional: Clean up resources
        pass


# Configuración del entorno para Stable-Baselines3
class SingleAgentWrapper(gym.Env):
    def __init__(self, env, agent_id):
        self.env = env
        self.agent_id = agent_id
        self.observation_space = env.observation_space(agent_id)
        self.action_space = env.action_space(agent_id)

    def reset(self, seed=None, options=None):
        obs, infos = self.env.reset(seed=seed, options=options)
        return obs[self.agent_id], infos[self.agent_id]

    def step(self, action):
        actions = {self.agent_id: action}
        obs, rewards, terminations, truncations, infos = self.env.step(actions)
        done = terminations[self.agent_id] or truncations[self.agent_id]
        return obs[self.agent_id], rewards[self.agent_id], terminations[self.agent_id], truncations[self.agent_id], infos[self.agent_id]

# Entrenamiento con Stable-Baselines3
if __name__ == "__main__":
    env = BusRouteMultiAgentEnv(route_data=dataset_df)
    single_agent_env = SingleAgentWrapper(env, agent_id=env.possible_agents[0])
    vec_env = make_vec_env(lambda: single_agent_env, n_envs=1)

    model = PPO("MlpPolicy", vec_env, verbose=1)
    model.learn(total_timesteps=100000)

    # Guardar el modelo entrenado
    model.save("bus_route_model")