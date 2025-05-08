def manage_buses(state, actions):
    """
    Modifica el número de camiones en las rutas según las acciones de los agentes.

    :param state: Diccionario que representa el estado actual del entorno.
    :param actions: Diccionario con las acciones de los agentes (0: quitar camión, 1: mantener, 2: agregar camión).
    :return: Estado actualizado con el número de camiones modificado.
    """
    for agent, action in actions.items():
        if action == 0:  # Quitar un camión
            state[agent]['buses'] = max(1, state[agent]['buses'] - 1)  # Asegurar al menos 1 camión
        elif action == 2:  # Agregar un camión
            state[agent]['buses'] += 1
    return state