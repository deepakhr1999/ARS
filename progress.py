import json
import os
from sklearn.model_selection import ParameterGrid
import pandas as pd

def load_config(env_name):
    config_path = f"configs/grids/{env_name}.json"
    with open(config_path, encoding="utf-8") as file:
        return json.load(file)


def main():
    ans = []
    for env in [
        "SafetySwimmerVelocity-v1",
        "SafetyHopperVelocity-v1",
        "SafetyHalfCheetahVelocity-v1",
        "SafetyWalker2dVelocity-v1",
        "SafetyAntVelocity-v1",
        "SafetyHumanoidVelocity-v1",
    ]:
        experiment_params_grid = load_config(env)
        experiment_params_grid["shift"] = [experiment_params_grid["shift"]]

        done = set()
        for experiment_params in ParameterGrid(experiment_params_grid):
            experiment_params["b"] = min(
                experiment_params["b"],
                experiment_params["N"]
            )
            key = json.dumps(experiment_params)
            done.add(key)
        path = f"data/{env}"
        ans.append((
            env.replace("Safety","").replace("Velocity-v1", ""),
            len(done),
            len(os.listdir(path)) if os.path.exists(path) else 0
        ))
    return pd.DataFrame(ans, columns=["task", "total", "completed"])

if __name__ == "__main__":

    print(main())

