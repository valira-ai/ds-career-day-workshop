import os

from typing import Any

import numpy as np
import pandas as pd
import psycopg


def make_dataset(out_path: str, features_config: dict[str, Any]) -> None:
    # for presentation purposes only, you should check data version, not just used cached one
    if os.path.exists(out_path):
        return

    conn = psycopg.connect(
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_URI"],
        port=os.environ["DB_PORT"],
    )

    data = pd.read_sql("SELECT * FROM vw_airbnb", con=conn)
    conn.close()

    data["price"] = data["price"].apply(lambda x: float(x.replace("$", "").replace(",", "")))
    data = data.replace(-1, np.nan)
    data = data.dropna()  # oops -> you should handle missing data, this is for presentation purposes only

    features_to_keep = [feat for feat in features_config.keys() if feat in set(data.columns)]
    data = data[features_to_keep]

    # data = data.rename(
    #     columns={
    #         "neighbourhood_name": "neighbourhood",
    #         "property_type_name": "prop_type",
    #         "room_type_name": "room_type",
    #         "accommodates": "num_people",
    #         "bed_type_name": "bed_type",
    #         "minimum_nights": "min_nights",
    #         "longitude": "lon",
    #         "latitude": "lat",
    #     }
    # )
    # data = data.drop(["city_id", "cancel_policy_name", "features", "listing_given_id", "amenities"], axis=1)

    # this should be in DB, ups
    # data["center_longitude"] = 2.320041
    # data["center_latitude"] = 48.85889

    data.to_parquet(out_path)
