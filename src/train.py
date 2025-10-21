import argparse
import warnings

from typing import Any

import joblib
import mlflow
import numpy as np
import pandas as pd
import yaml

from dotenv import load_dotenv
from scipy.stats import bootstrap
from sklearn.model_selection import train_test_split

from airbnb_model.data.make_dataset import make_dataset
from airbnb_model.data.feature_pipeline import parse_target_from_config

from airbnb_model.model import create_model_pipeline


def train(train_config: dict[str, Any], model_config: dict[str, Any], features_config: dict[str, Any]) -> None:
    mlflow.log_params(model_config)
    mlflow.log_params(train_config)
    mlflow.log_params(features_config)

    # READ DATA
    make_dataset(train_config["data_path"], features_config)
    data = pd.read_parquet(train_config["data_path"])

    target_col = parse_target_from_config(features_config)
    df = data.drop(target_col, axis=1)
    target = data[target_col]
    X_train, X_test, y_train, y_test = train_test_split(
        df, target, test_size=train_config["test_size"], random_state=train_config["seed"]
    )

    model_pipeline = create_model_pipeline(model_config, features_config, model_config["feature_slots"])
    model_pipeline.fit(X_train, y_train)

    y_pred = model_pipeline.predict(X_test)

    # EVALUATION
    maes = np.abs(y_test - y_pred)
    res = bootstrap((maes,), np.mean, n_resamples=train_config["num_bootstrap"])
    print(f"MAE: {np.mean(maes):.4f}, ({res.confidence_interval.low:.4f}, {res.confidence_interval.high:.4f})")
    mlflow.log_metric("mae", np.mean(maes))
    mlflow.log_metric("mae-low", res.confidence_interval.low)
    mlflow.log_metric("mae-high", res.confidence_interval.high)

    mses = maes**2
    res = bootstrap((mses,), np.mean, n_resamples=train_config["num_bootstrap"])
    print(f"MSE: {np.mean(mses):.4f}, ({res.confidence_interval.low:.4f}, {res.confidence_interval.high:.4f})")
    mlflow.log_metric("mse", np.mean(mses))
    mlflow.log_metric("mse-low", res.confidence_interval.low)
    mlflow.log_metric("mse-high", res.confidence_interval.high)

    # SAVE MODEL
    joblib.dump(model_pipeline, train_config["output_path"])
    mlflow.log_artifact(train_config["output_path"])


def _setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Training parser")

    parser.add_argument("--train_config_path", type=str, default="config/train.yaml")
    parser.add_argument("--features_config_path", type=str, default="config/features.yaml")

    return parser


if __name__ == "__main__":
    # Filter sklearn pipeline warnings
    warnings.filterwarnings("ignore", message="This Pipeline instance is not fitted yet", category=FutureWarning)
    
    # setup
    load_dotenv(".env")
    args = _setup_parser().parse_args()

    with open(args.train_config_path, "r") as f:
        run_config = yaml.load(f, Loader=yaml.FullLoader)

    model_config = run_config.get(run_config["model"], None)
    if model_config is None:
        print("Model configuration doesn't exist.")
        exit(1)

    with open(args.features_config_path, "r") as f:
        features_config = yaml.load(f, Loader=yaml.FullLoader)

    with mlflow.start_run():
        train(run_config["params"], model_config, features_config)
