from typing import Any

from typing import Any

from sklearn.base import BaseEstimator
from sklearn.linear_model import Ridge
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor
import mlflow

from airbnb_model.data.feature_pipeline import create_data_pipeline
from airbnb_model.utils import _filter_config


class MLPRegressorWithLogging(MLPRegressor):
    """MLPRegressor that logs training loss to MLflow during training"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def fit(self, X, y):
        # Override fit to log losses during training
        result = super().fit(X, y)
        
        # Log training loss curve to MLflow (always available)
        if hasattr(self, 'loss_curve_') and self.loss_curve_ is not None:
            for epoch, loss in enumerate(self.loss_curve_):
                mlflow.log_metric("training_loss", loss, step=epoch)
            
            # Log final training info
            mlflow.log_metrics({
                "final_training_loss": self.loss_curve_[-1],
                "n_epochs": len(self.loss_curve_),
                "converged": self.n_iter_ < self.max_iter
            })
        
        # Log validation loss if available (only when early_stopping=True)
        if (hasattr(self, 'validation_scores_') and 
            self.validation_scores_ is not None):
            for epoch, val_loss in enumerate(self.validation_scores_):
                mlflow.log_metric("validation_loss", val_loss, step=epoch)
                
            mlflow.log_metric("final_validation_loss", self.validation_scores_[-1])
        
        # Log model architecture info
        mlflow.log_params({
            "n_layers": len(self.hidden_layer_sizes) + 1,
            "total_parameters": sum([layer.size for layer in self.coefs_]),
            "n_features_in": self.n_features_in_,
            "n_outputs": self.n_outputs_
        })
                
        return result


def _create_model(model_config: dict[str, Any]) -> BaseEstimator:
    if model_config["type"] == "xgboost":
        model_config = _filter_config(model_config, XGBRegressor)
        return XGBRegressor(**model_config)
    elif model_config["type"] == "ridge":
        model_config = _filter_config(model_config, Ridge)
        return Ridge(**model_config)
    elif model_config["type"] == "mlp":
        model_config = _filter_config(model_config, MLPRegressorWithLogging)
        return MLPRegressorWithLogging(**model_config)
    else:
        raise NotImplementedError


def create_model_pipeline(
    model_config: dict[str, Any], features_config: dict[str, Any], feature_slots: list[str]
) -> Pipeline:
    model_pipeline = Pipeline(
        [
            ("data_pipeline", create_data_pipeline(features_config, feature_slots)),
            ("model", _create_model(model_config)),
        ]
    )

    return model_pipeline
