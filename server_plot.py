
import sys
sys.path.append("code")
from plotting import update_layout
import glob
import pandas as pd
import plotly.express as px
import json

def main():
    records = []
    for experiment_file in glob.glob("sfr2/*/*/params.json", recursive=True):
        with open(experiment_file, "r", encoding="utf-8") as file:
            record = json.load(file)
            if "Walker" not in record["env_name"]:
                continue
            records.append(record)

    all_data = pd.DataFrame.from_records(records)

    def get_best_reward(dir_path):
        try:
            x = pd.read_csv(dir_path+"/log.txt", sep="\t")
            return x["AverageReward"].max()
        except:
            return -1

    def get_time_taken(dir_path):
        try:
            x = pd.read_csv(dir_path+"/log.txt", sep="\t")
            return x["Time"].max() / 3600
        except:
            return -1

    def label_algorithm(filter):
        if filter == "MeanStdFilter":
            return "SFR-v2"
        return "SFR-v1"

    all_data['reward'] = all_data.dir_path.apply(get_best_reward)
    all_data['time'] = all_data.dir_path.apply(get_time_taken)
    all_data = all_data[all_data.reward > 0]
    all_data['task'] = all_data.env_name.str.replace("Safety", '').str.replace("Velocity-v1", '')
    all_data["algo"] = all_data["filter"].apply(label_algorithm)

    all_data['best_env_reward'] = all_data.groupby(["task", "algo", "transform"]).reward.transform('max')
    data = (
        all_data[all_data.reward == all_data.best_env_reward]
        .reset_index(drop=True)
        .drop(["filter", "policy_type", "rollout_length", "shift", "best_env_reward", "env_name"], axis=1)
    )

    data["best_reward"] = data.groupby(["task", "algo", "transform"]).reward.transform('max')
    best_data = data[data.reward == data.best_reward].reset_index(drop=True)
    best_data

    for (task, algo), data1 in best_data.groupby(["task", "algo"]):
        frames = []
        for filename, transform, algo in zip(data1.dir_path, data1['transform'], data1["algo"]):
            x = pd.read_csv(filename+"/log.txt", sep="\t")[["AverageReward", "timesteps"]]
            x["task"] = task
            x["algo"] = algo
            x["transform"] = transform
            frames.append(x)
        frame = pd.concat(frames, ignore_index=True).sort_values(["transform", "timesteps"], ignore_index=True)


        frame.rename({
            'timesteps': "steps",
            'AverageReward': "reward"
        }, axis=1, inplace=True)
        frame.steps = frame.steps.astype(int)
        fig = px.line(data_frame=frame, x="steps", y="reward", color="transform")
        fig.update_traces(opacity=.7)
        update_layout(fig, task + ": " + algo, "Timesteps", "Reward", row=1, col=1, upkwargs=dict(width=1000, height=800))
        fig.update_yaxes(range=[0, None])
        fig.write_image(f"static/{task}_{algo}.png", scale=1)

    time_taken = all_data.groupby("task")["time"].max().round(2).reset_index()
    time_taken.columns = ["task", "Time"]
    return best_data[["algo", "task", "best_reward", "transform"]], time_taken


if __name__ == "__main__":
    main()
