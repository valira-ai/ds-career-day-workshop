import argparse
import itertools

import mlflow
import yaml

from dotenv import load_dotenv

from train import train


def _setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Training parser")

    parser.add_argument("--grid_config_path", type=str, default="config/grid_search.yaml")
    parser.add_argument("--features_config_path", type=str, default="config/features.yaml")

    return parser


if __name__ == "__main__":
    # setup
    load_dotenv(".env")
    args = _setup_parser().parse_args()

    with open(args.grid_config_path, "r") as f:
        grid_config = yaml.load(f, Loader=yaml.FullLoader)

    with open(args.features_config_path, "r") as f:
        features_config = yaml.load(f, Loader=yaml.FullLoader)

    with mlflow.start_run(nested=True):
        for model in grid_config["models"]:
            type_ = grid_config[model]["type"]
            feature_slots = grid_config[model]["feature_slots"]
            del grid_config[model]["type"], grid_config[model]["feature_slots"]

            keys, values = zip(*grid_config[model].items())
            all_configs = [dict(zip(keys, v)) for v in itertools.product(*values)]
            for model_config in all_configs:
                model_config["type"] = type_
                model_config["feature_slots"] = feature_slots
                with mlflow.start_run(nested=True):
                    train(grid_config["params"], model_config, features_config)
