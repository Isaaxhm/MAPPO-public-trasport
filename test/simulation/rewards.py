def calculate_rewards(state):
    rewards = {}
    for agent, data in state.items():
        rewards[agent] = -data['headway'] + data['demand'] * 0.1
    return rewards