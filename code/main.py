import argparse
import json
import time
from ars import run_ars
import ray


def parse_arguments():
    parser = argparse.ArgumentParser(description="Run an ARS experiment.")
    parser.add_argument(
        "env_name",
        type=str,
        help="Environment ID to run the experiment on.",
        choices=[
            "SafetySwimmerVelocity-v1",
            "SafetyHopperVelocity-v1",
            "SafetyHalfCheetahVelocity-v1",
            "SafetyWalker2dVelocity-v1",
            "SafetyAntVelocity-v1",
            "SafetyHumanoidVelocity-v1",
        ],
    )
    return parser.parse_args()


def load_config(env_name):
    config_path = f"configs/{env_name}.json"
    with open(config_path, encoding="utf-8") as file:
        return json.load(file)


def main():
    args = parse_arguments()
    config = load_config(args.env_name)

    experiment_params = {
        "env_name": args.env_name,
        "n_iter": 1000,
        "n_directions": config["N"],
        "deltas_used": config["b"],
        "step_size": config["alpha"],
        "delta_std": config["nu"],
        "n_workers": 10,
        "rollout_length": 1000,
        "shift": config["shift"],
        "seed": 237,
        "policy_type": "linear",
        "dir_path": f"data/{args.env_name}/{time.time()}",
        "filter": "MeanStdFilter",
    }

    for seed in range(4):
        experiment_params["seed"] = seed
        run_ars(experiment_params)


if __name__ == "__main__":
    ray.init()
    main()
