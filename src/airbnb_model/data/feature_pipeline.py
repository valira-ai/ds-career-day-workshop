from typing import Any

from geopy.distance import great_circle
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline


class FeatureSelector(BaseEstimator, TransformerMixin):
    def __init__(self, feature_names: list[str]) -> None:
        self.feature_names = feature_names

    def fit(self, X, y=None):
        self.feature_names = set(self.feature_names)
        return self

    def transform(self, X, y=None):
        return X.loc[:, list(self.feature_names.intersection(X.columns))].copy(deep=True)

    def set_output(self, *, transform=None):
        return self


class CreateLongitudeLatitudeFeatures(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X.loc[:, "longitude_to_center"] = X.apply(lambda x: x["longitude"] - x["center_longitude"], axis=1)
        X.loc[:, "latitude_to_center"] = X.apply(lambda x: x["latitude"] - x["center_latitude"], axis=1)

        X.loc[:, "distance_to_center"] = X.apply(
            lambda x: great_circle((x["latitude"], x["longitude"]), (x["center_latitude"], x["center_longitude"])).km,
            axis=1,
        )

        return X

    def set_output(self, *, transform=None):
        return self


def _parse_features_config(features_config: dict[str, Any], feature_slots: list[str]) -> tuple[list[str], ...]:
    slots = set(feature_slots)

    numerical_features = [feat for feat, type_ in features_config.items() if type_ == "numerical" and feat in slots]
    categorical_features = [feat for feat, type_ in features_config.items() if type_ == "categorical" and feat in slots]
    logical_features = [feat for feat, type_ in features_config.items() if type_ == "logical" and feat in slots]

    return numerical_features, categorical_features, logical_features


def parse_target_from_config(features_config: dict[str, Any]) -> str:
    target_list = [feature for feature, type_ in features_config.items() if type_ == "target"]
    assert len(target_list) == 1, "There must be a single target column"

    return target_list[0]


def create_data_pipeline(features_config: dict[str, Any], feature_slots: list[str]) -> Pipeline:
    numerical_features, categorical_features, logical_features = _parse_features_config(features_config, feature_slots)

    long_lat_features = Pipeline(
        [
            ("feaure_creator", CreateLongitudeLatitudeFeatures()),
            ("post_select", FeatureSelector(["longitude_to_center", "latitude_to_center", "distance_to_center"])),
        ]
    )
    cols = ["longitude", "latitude", "center_longitude", "center_latitude"]
    feature_engineering_pipeline = ColumnTransformer(
        [("feature_engineering", long_lat_features, cols)], remainder="passthrough", verbose_feature_names_out=False
    )
    feature_engineering_pipeline.set_output(transform="pandas")

    preprocessing_pipeline = ColumnTransformer(
        [
            ("numerical", StandardScaler(), numerical_features),
            ("categorical", OneHotEncoder(drop="first", handle_unknown="ignore"), categorical_features),
            ("logical", FeatureSelector(logical_features), logical_features),
        ],
        remainder="drop",
    )
    data_pipeline = Pipeline(
        [
            ("feature_engineering", feature_engineering_pipeline),
            ("preprocessing", preprocessing_pipeline),
        ]
    )

    return data_pipeline
