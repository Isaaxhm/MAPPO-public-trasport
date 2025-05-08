from test.simulation.agent_actions import apply_agent_actions
from test.simulation.manage_buses import manage_buses
from test.simulation.rewards import calculate_rewards
from gym.spaces import Discrete, Box

class BusRouteMultiAgentEnv:
    def __init__(self, route_data):
        self.route_data = route_data
        self.state = self._initialize_state()
        self.agents = list(self.state.keys())
        self.action_space = Discrete(5)  # Ejemplo: 5 acciones posibles
        self.observation_space = Box(low=0, high=100, shape=(1,), dtype=int)  # Ajustar rango de valores esperados

    def _initialize_state(self):
        state = {}
        for _, row in self.route_data.iterrows():
            state[row['route']] = {
                'buses': row['buses'],
                'headway': row['headway'],
                'speed': row['speed'],
                'demand': row['demand']
            }
        return state

    def reset(self):
        self.state = self._initialize_state()
        return self.state

    def step(self, actions):
        self.state = apply_agent_actions(self.state, actions)
        self.state = manage_buses(self.state, actions)
        rewards = calculate_rewards(self.state)
        dones = {agent: False for agent in self.agents}  # Ejemplo: ningún agente termina
        info = {}  # Información adicional vacía
        return self.state, rewards, dones, info