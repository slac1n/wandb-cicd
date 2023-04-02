import wandb

# print wandb version
print(f"Wandb version: {wandb.__version__}")
assert wandb.__version__=="0.14.0", f"Expected wandb verion 0.14.0, got {wandb.__version__}"
