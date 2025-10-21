import argparse
import itertools

import mlflow
import yaml
import warnings

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
    
    # Filter sklearn pipeline warnings
    warnings.filterwarnings("ignore", message="This Pipeline instance is not fitted yet", category=FutureWarning)

    with open(args.grid_config_path, "r") as f:
        grid_config = yaml.load(f, Loader=yaml.FullLoader)

    with open(args.features_config_path, "r") as f:
        features_config = yaml.load(f, Loader=yaml.FullLoader)

    # Parent run for the entire grid search experiment
    with mlflow.start_run(run_name="Grid_Search_Experiment") as parent_run:
        mlflow.log_params({"experiment_type": "grid_search", "models": grid_config["models"]})
        
        best_mae = float('inf')
        best_run_id = None
        best_model_path = None
        
        for model in grid_config["models"]:
            type_ = grid_config[model]["type"]
            feature_slots = grid_config[model]["feature_slots"]
            del grid_config[model]["type"], grid_config[model]["feature_slots"]

            keys, values = zip(*grid_config[model].items())
            all_configs = [dict(zip(keys, v)) for v in itertools.product(*values)]
            
            for i, model_config in enumerate(all_configs):
                model_config["type"] = type_
                model_config["feature_slots"] = feature_slots
                
                run_name = f"{model}_{i+1}_" + "_".join([f"{k}={v}" for k, v in model_config.items() if k not in ["type", "feature_slots"]])
                
                # Create unique model path for each run
                model_path = f"models/model_{model}_{i+1}.joblib"
                temp_params = grid_config["params"].copy()
                temp_params["output_path"] = model_path
                
                with mlflow.start_run(nested=True, run_name=run_name) as child_run:
                    train(temp_params, model_config, features_config)
                    
                    # Track best model
                    current_mae = mlflow.get_run(child_run.info.run_id).data.metrics.get("mae", float('inf'))
                    if current_mae < best_mae:
                        best_mae = current_mae
                        best_run_id = child_run.info.run_id
                        best_model_path = model_path
        
        # Copy the best model to the standard location
        if best_model_path:
            import shutil
            shutil.copy2(best_model_path, "models/model.joblib")
            print(f"Best model copied to models/model.joblib")
        
        # Log best model info to parent run
        mlflow.log_metrics({"best_mae": best_mae})
        mlflow.log_params({"best_run_id": best_run_id, "best_model_path": best_model_path})
        print(f"Best model MAE: {best_mae:.4f} (Run ID: {best_run_id})")
