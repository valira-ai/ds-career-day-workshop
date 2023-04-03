from typing import Any

from sklearn.base import BaseEstimator
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor

from airbnb_model.data.feature_pipeline import create_data_pipeline
from airbnb_model.utils import _filter_config


def _create_model(model_config: dict[str, Any]) -> BaseEstimator:
    if model_config["type"] == "xgboost":
        return XGBRegressor(**model_config)
    elif model_config["type"] == "ridge":
        model_config = _filter_config(model_config, Ridge)
        return Ridge(**model_config)
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
