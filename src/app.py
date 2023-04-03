import joblib
import pandas as pd
import pydantic

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder


app = FastAPI(title="AirBnB price prediction")
model = joblib.load("../models/model.joblib")

city_centers = {"Paris": {"lon": 2.320041, "lat": 48.85889}}  # very dirty, should load from DB


class InputData(pydantic.BaseModel):
    city: str
    neighbourhood_name: str
    property_type_name: str
    room_type_name: str
    bed_type_name: str
    accommodates: int
    bathrooms: int
    bedrooms: int
    beds: int
    minimum_nights: int
    longitude: float
    latitude: float


class OutputData(pydantic.BaseModel):
    predicted_price: float


@app.post("/predict", response_model=OutputData)
async def predict(data: InputData):
    data_dict = jsonable_encoder(data)
    data_dict["center_longitude"] = city_centers[data_dict["city"]]["lon"]
    data_dict["center_latitude"] = city_centers[data_dict["city"]]["lat"]
    del data_dict["city"]

    input_data = pd.DataFrame([data_dict])
    prediction = model.predict(input_data)

    return {"predicted_price": prediction}
