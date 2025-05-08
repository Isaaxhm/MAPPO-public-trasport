from test.simulation.agent_actions import apply_agent_actions
from test.simulation.manage_buses import manage_buses
from test.simulation.rewards import calculate_rewards

class BusRouteMultiAgentEnv:
    def __init__(self, route_data):
        self.route_data = route_data
        self.state = self._initialize_state()
        self.agents = list(self.state.keys())

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
        return self.state, rewards