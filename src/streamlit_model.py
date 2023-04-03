import pandas as pd
import requests
import streamlit as st


def get_predicted_price():
    request_data = {
        "city": "Paris",
        "neighbourhood_name": st.session_state["neighbourhood"],
        "property_type_name": st.session_state["prop_type"],
        "room_type_name": st.session_state["room_type"],
        "accommodates": st.session_state["num_people"],
        "bathrooms": st.session_state["bathrooms"],
        "bedrooms": st.session_state["bedrooms"],
        "beds": st.session_state["beds"],
        "bed_type_name": st.session_state["bed_type"],
        "minimum_nights": st.session_state["min_nights"],
        "longitude": st.session_state["lon"],
        "latitude": st.session_state["lat"],
    }

    st.session_state["price"] = requests.post("http://localhost:8000/predict", json=request_data).json()[
        "predicted_price"
    ]


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    data = pd.read_parquet(path)

    return data


data = load_data("data/raw.parquet")

if "neighbourhood" not in st.session_state:
    st.session_state["neighbourhood"] = "Buttes-Montmartre"
if "prop_type" not in st.session_state:
    st.session_state["prop_type"] = "Condominium"
if "room_type" not in st.session_state:
    st.session_state["room_type"] = "Entire home/apt"
if "num_people" not in st.session_state:
    st.session_state["num_people"] = 2
if "bathrooms" not in st.session_state:
    st.session_state["bathrooms"] = 1
if "bedrooms" not in st.session_state:
    st.session_state["bedrooms"] = 1
if "beds" not in st.session_state:
    st.session_state["beds"] = 1
if "bed_type" not in st.session_state:
    st.session_state["bed_type"] = "Real Bed"
if "min_nights" not in st.session_state:
    st.session_state["min_nights"] = 1
if "lon" not in st.session_state:
    st.session_state["lon"] = 2.336867
if "lat" not in st.session_state:
    st.session_state["lat"] = 48.894187

if "price" not in st.session_state:
    st.session_state["price"] = "/"

st.title("How much should you charge for a night in Paris?")
st.write("Location:")
st.session_state["neighbourhood"] = st.selectbox("Neighbourhood:", options=data["neighbourhood_name"].unique())
st.session_state["lat"] = st.slider("Latitude:", data["latitude"].min(), data["latitude"].max(), 48.894187)
st.session_state["lon"] = st.slider("Longitude:", data["longitude"].min(), data["longitude"].max(), 2.336867)

st.write("Property information:")
st.session_state["prop_type"] = st.selectbox("Property type", options=data["property_type_name"].unique())
st.session_state["room_type"] = st.selectbox("Room type", options=data["room_type_name"].unique())

st.session_state["num_people"] = st.slider(
    "How many people can it accomodate?", int(data["accommodates"].min()), int(data["accommodates"].max()), 2
)
st.session_state["bathrooms"] = st.slider(
    "How many bathrooms are in your listing?", int(data["bathrooms"].min()), int(data["bathrooms"].max()), 1
)
st.session_state["bedrooms"] = st.slider(
    "How many bedrooms are in your listing?", int(data["bedrooms"].min()), int(data["bedrooms"].max()), 1
)
st.session_state["beds"] = st.slider(
    "How many beds are in your listing?", int(data["beds"].min()), int(data["beds"].max()), 1
)
st.session_state["min_nights"] = st.number_input(
    "Minimal nights for a stay?", int(data["minimum_nights"].min()), int(data["minimum_nights"].max()), 1
)


if st.button("Calculate price"):
    get_predicted_price()
st.text(f"Price should be {st.session_state['price']} dollars.")
