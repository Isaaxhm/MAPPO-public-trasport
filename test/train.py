import ray
from ray import tune
from ray.rllib.algorithms.ppo import PPOConfig
from env import TransitRoutesEnv
import yaml

# Cargar datos de configuración
with open("configs/mappo_config.yaml") as f:
    config = yaml.safe_load(f)

route_data = config['route_data']
num_agents = len(route_data)

# Inicialización Ray
ray.init()

# Registrar el entorno
from ray.tune.registry import register_env
register_env("TransitRoutesEnv", lambda cfg: TransitRoutesEnv(route_data))

# Configurar MAPPO (PPO con crítico centralizado)
ppo_config = (
    PPOConfig()
    .environment(env="TransitRoutesEnv")
    .framework("torch")
    .rollouts(num_rollout_workers=4)
    .training(
        model={
            "custom_model": "route_central_critic",
            "custom_model_config": {"num_agents": num_agents}
        },
        centralized_critic=True
    )
    .multi_agent(
        policies={"shared_policy": (None, TransitRoutesEnv(route_data).observation_space,
                                     TransitRoutesEnv(route_data).action_space, {})},
        policy_mapping_fn=lambda aid, **kwargs: "shared_policy"
    )
)

# Ejecutar entrenamiento
tuner = tune.Tuner(
    "PPO",
    param_space=ppo_config.to_dict(),
    run_config=tune.RunConfig(stop={"training_iteration": 50})
)
tuner.fit()