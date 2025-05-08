def calculate_rewards(state):
    rewards = {}
    for agent, data in state.items():
        headway = float(data['headway'].replace('min', '').strip()) if isinstance(data['headway'], str) else data['headway']
        demand = float(data['demand']) if isinstance(data['demand'], str) else data['demand']
        rewards[agent] = -headway + demand * 0.1
    return rewards