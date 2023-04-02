import wandb

# print wandb version
print(f"Wandb version: {wandb.__version__}")
assert wandb.__version__=="1.1.0", f"Expected wandb verion 1.1.0, got {wandb.__version__}"
