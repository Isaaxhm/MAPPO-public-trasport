from ray.rllib.models import ModelCatalog
from ray.rllib.models.torch.torch_modelv2 import TorchModelV2
from ray.rllib.utils.typing import ModelConfigDict
import torch.nn as nn
import torch

class RouteCentralizedCritic(TorchModelV2, nn.Module):
    def __init__(self, obs_space, action_space, num_outputs, model_config: ModelConfigDict, name):
        TorchModelV2.__init__(self, obs_space, action_space, num_outputs, model_config, name)
        nn.Module.__init__(self)
        self.num_agents = model_config['custom_model_config']['num_agents']

        # MLP para cada observación local
        self.shared_fc = nn.Sequential(
            nn.Linear(4, 64), nn.ReLU(),
            nn.Linear(64, 64), nn.ReLU()
        )
        # Cabeza de valor que toma concat de features de todos los agentes
        self.value_head = nn.Linear(64 * self.num_agents, 1)

    def forward(self, input_dict, state, seq_lens):
        # input_dict['obs'] shape: [B, 4]
        x = input_dict["obs_flat"] if "obs_flat" in input_dict else input_dict["obs"]
        # Features locales: [B, 64]
        feat = self.shared_fc(x)
        # Guardar temporal para value_function
        self._last_flat = feat
        return feat, state

    def value_function(self):
        # Suponer que _last_flat contiene [B*num_agents, 64]
        # Reagrupar y concatenar
        batch_size = self._last_flat.shape[0] // self.num_agents
        feat = self._last_flat.view(batch_size, self.num_agents * 64)
        return self.value_head(feat).squeeze(1)

# Registrar el modelo
ModelCatalog.register_custom_model("route_central_critic", RouteCentralizedCritic)