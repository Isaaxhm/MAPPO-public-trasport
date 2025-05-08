class Logger:
    def __init__(self, workbook, worksheet):
        self.workbook = workbook
        self.worksheet = worksheet
        self.row = 1

    def log_metrics(self, iteration, logger):
        metrics = logger.name_to_value
        data = [
            iteration,
            metrics.get('time/total_timesteps', 0),
            metrics.get('time/fps', 0),
            metrics.get('rollout/ep_len_mean', 0),
            metrics.get('rollout/ep_rew_mean', 0),
            metrics.get('train/loss', 0),
            metrics.get('train/value_loss', 0),
            metrics.get('train/policy_gradient_loss', 0)
        ]
        for col, value in enumerate(data):
            self.worksheet.write(self.row, col, value)
        self.row += 1