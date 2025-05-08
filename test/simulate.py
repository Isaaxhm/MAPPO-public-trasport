import pandas as pd
from src.env.bus_route_env import BusRouteMultiAgentEnv

def run_simulation():
    # Cargar datos de rutas
    data_path = "data/route_summaries.txt"
    data = []
    with open(data_path, 'r') as file:
        for line in file:
            if line.startswith("Route"):
                parts = line.split(": ")
                route_name = parts[0].split(" ")[1]
                metrics = {k: float(v.replace("min", "")) for k, v in (item.split("=") for item in parts[1].split(", "))}
                data.append({"route": route_name, **metrics})

    route_data = pd.DataFrame(data)

    # Crear entorno
    env = BusRouteMultiAgentEnv(route_data)
    obs, _ = env.reset()

    for step in range(100):
        actions = {agent: env.action_space(agent).sample() for agent in env.agents}
        obs, rewards, terminations, truncations, infos = env.step(actions)
        print(f"Step {step}: Rewards: {rewards}")

if __name__ == "__main__":
    run_simulation()