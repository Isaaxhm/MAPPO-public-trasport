from test.training.logger import setup_logger
from test.training.environment import create_environment
from stable_baselines3 import PPO

if __name__ == "__main__":
    # Configurar el entorno y el logger
    env, logger, workbook, worksheet = create_environment()

    # Crear el modelo PPO
    model = PPO("MlpPolicy", env, verbose=1)

    # Entrenar el modelo
    for iteration in range(1, 101):
        model.learn(total_timesteps=2048, reset_num_timesteps=False)
        logger.log_metrics(iteration, model.logger)

    # Guardar el modelo entrenado
    model.save("bus_route_model")

    # Cerrar el archivo Excel
    workbook.close()