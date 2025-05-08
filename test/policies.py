import random

def random_policy(observation):
    return random.choice([0, 1, 2])  # Acciones: 0 (Disminuir), 1 (Mantener), 2 (Aumentar)