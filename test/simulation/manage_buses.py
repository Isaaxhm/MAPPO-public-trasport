def manage_buses(state, actions):
    for agent, action in actions.items():
        if action == 0:  # Quitar un camión
            state[agent]['buses'] = max(1, state[agent]['buses'] - 1)
        elif action == 2:  # Agregar un camión
            state[agent]['buses'] += 1
    return state