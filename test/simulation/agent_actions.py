def apply_agent_actions(state, actions):
    for agent, action in actions.items():
        if action == 0:  # Disminuir velocidad
            state[agent]['speed'] = max(0, state[agent]['speed'] - 0.01)
        elif action == 1:  # Mantener velocidad
            pass
        elif action == 2:  # Aumentar velocidad
            state[agent]['speed'] += 0.01
    return state