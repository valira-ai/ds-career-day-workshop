# Data Science Project: From Idea to Execution :hammer_and_wrench:	
Materials for the Data Science Career Day Workshop that is being held on Tuesday, October 21 2025, at the Faculty of Computer and Information Science, University of Ljubljana. The purpose of the workshop was to demonstrate the whole workflow in data science-related applications.

Link to data: https://drive.google.com/file/d/1Ek_ozlNE2B5B6VR2ulKsM3XaQ1oXSIgx/view?usp=sharing

## Airbnb Paris: how much can I charge? :money_with_wings:
Imagine you have a spare apartment in Paris and you want to list in on Airbnb. However, you do not know a lot about Paris real estate prices, so that is a problem! If you charge too much, you will get less bookings, if you charge too little, you will have less profit! Luckily, you can call your friends *data engineer*, *data scientist* and *ML engineer* to help you out.  

They built the whole pipeline for you from scratch, from data collection all the way to model deployment. In the end they made you a nice web app, where you can input the characteristics of your apartment and you get the suggested price. :star_struck:	

That's not all! They were also kind enough to write instructions for you, so you can run it yourself:

### 1. Data engineer
As data engineers our task in this project is to collect & store data and prepare everything for the data scientist.  
The code can be found in the [`./notebooks/01_data_engineer.ipynb`](https://github.com/valira-ai/ds-career-day-workshop/blob/main/notebooks/01_data_engineer.ipynb) notebook, however, in order to run it we first need to set up our own Postgres database.

#### Database setup
There are plenty of resources online guiding us how to set up our [PostgresSQL](https://www.postgresql.org/) database. For example we could do it [locally](https://www.codecademy.com/article/installing-and-using-postgresql-locally) or in the cloud ([AWS](https://aws.amazon.com/getting-started/hands-on/create-connect-postgresql-db/) free tier is enough for our purposes). When the server is up and running, we can connect to it and create our database. We suggest using [pgAdmin](https://www.pgadmin.org/), a GUI tool made for interacting with the Postgres database sessions. In the [`./sql/`](https://github.com/valira-ai/ds-career-day-workshop/tree/main/sql) folder we can find SQL scripts that will set up the database tables, stored procedures and views for us and voilà! We are ready to run the notebook and pass the torch on to the data scientist.

### 2. Data scientist
As data scientists we perform exploratory data analysis (EDA), feature engineering, feature selection, model selection, metric selection, model validation and prepare the report. The code including most of these steps can be found in the [`./notebooks/02_data_science.ipynb`](https://github.com/valira-ai/ds-career-day-workshop/blob/main/notebooks/02_data_science.ipynb) notebook. In order to run it we require access to the database from the previous step.

### 3. ML Engineer
In this project, the role of a ML Engineer is to productionalize and package the model code, set up experiment tracking, model registry and deploy the model to production. Throughout our tasks we build on previous work of both data engineers and data scientists. Our code is in [`src/`](https://github.com/valira-ai/ds-career-day-workshop/tree/main/src) directory, the model package is in [`src/airbnb_model`](https://github.com/valira-ai/ds-career-day-workshop/tree/main/src/airbnb_model).

You can follow these steps to reproduce the work.

**Setup**

Create python virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
```
Install our project in editable mode:
```bash
pip install -e .
```

Create .env file based on default.env, change variables to reflect you PostgresSQL set up.

**Training**

Train a model (based on `config/train.yaml`):
```bash
python src/train.py
```

Perform grid search (based on `config/grid_search.yaml`):
```bash
python src/multi_train.py
```

All of our runs are logged by **mlflow** (in `mlruns/` folder). You can run a mlflow dashboard with:
```bash
mlflow ui
```
Go to *http://127.0.0.1:5000/* (by default) to see the dashboard.

**Deployment**

You can deploy our model locally by launching the server with:
```bash
cd src
uvicorn app:app --port 8000
```
Optionally, you can use Docker to containerize the deployment with:
```bash
docker build -t model-api .
docker run -d --name model-serving -p 8000:8000 model-api
```

We can check the docs of our deployed API by going to *http://localhost:8000/docs*.

To test if the model API works, we can use curl with some default values:
```bash
curl -H "Content-Type: application/json" -d '{
  "city": "Paris",
  "neighbourhood_name": "Buttes-Montmartre",
  "property_type_name": "Condominium",
  "room_type_name": "Entire home/apt",
  "accommodates": 2,
  "bathrooms": 1,
  "bedrooms": 1,
  "beds": 1,
  "bed_type_name": "Real Bed",
  "minimum_nights": 1,
  "longitude": 2.336867,
  "latitude": 48.894187  
}' -XPOST localhost:8000/predict
```
which should return a JSON with the predicted price.

We can use Streamlit to provide a frontend that showcases our model. We can run the Streamlit app with:
```bash
streamlit run src/streamlit_model.py
```
