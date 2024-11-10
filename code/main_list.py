import argparse
import json
import time
from ars import run_ars
import ray
from sklearn.model_selection import ParameterGrid


def load_config():
    with open("to_run.json", encoding="utf-8") as file:
        return json.load(file)


def main():

    for experiment_params in load_config():
        experiment_params["deltas_used"] = min(
            experiment_params["deltas_used"], experiment_params["n_directions"]
        )
        print("Running for params")
        print(json.dumps(experiment_params, indent=4))
        experiment_params["dir_path"] = (
            f"data/{experiment_params['env_name']}/{time.time()}"
        )
        run_ars(experiment_params)


if __name__ == "__main__":
    ray.init()
    main()
