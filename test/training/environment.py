import xlsxwriter
from test.simulation.environment import BusRouteMultiAgentEnv
from stable_baselines3.common.env_util import make_vec_env

def create_environment():
    # Crear un archivo Excel para guardar los resultados
    workbook = xlsxwriter.Workbook('training_results.xlsx')
    worksheet = workbook.add_worksheet()

    # Escribir encabezados en el archivo Excel
    headers = ['Iteration', 'Total Timesteps', 'FPS', 'Episode Length Mean', 'Episode Reward Mean', 'Loss', 'Value Loss', 'Policy Gradient Loss']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    # Configurar el entorno
    env = BusRouteMultiAgentEnv(route_data=dataset_df)
    single_agent_env = SingleAgentWrapper(env, agent_id=env.possible_agents[0])
    vec_env = make_vec_env(lambda: single_agent_env, n_envs=1)

    return vec_env, Logger(workbook, worksheet), workbook, worksheet