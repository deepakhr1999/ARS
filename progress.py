import os
from sklearn.model_selection import ParameterGrid
import json

def get_total_runs(env_name):
    config_path = f"configs/grids/{env_name}.json"
    with open(config_path, encoding="utf-8") as file:
        grid = json.load(file)
    grid["shift"] = [grid["shift"]]
    grid = ParameterGrid(grid)
    return len(grid)

for env_name in os.listdir("data"):
    total_runs = get_total_runs(env_name)
    runs_done = len(os.listdir(f"data/{env_name}/")) - 4
    percentage_completed = round(100 * runs_done / total_runs, 2)
    print(env_name.ljust(30), f"{runs_done}/{total_runs}".rjust(8), f"{percentage_completed:.2f}%".rjust(10))
