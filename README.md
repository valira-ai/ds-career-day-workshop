# Data Science Project: From Idea to Execution :hammer_and_wrench:	
Materials for the Data Science Career Day Workshop that was held on Wednesday, March 23 2023, at the Faculty of Computer and Information Science, University of Ljubljana. The purpose of the workshop was to demonstrate the whole workflow in data science-related applications.

## Airbnb Paris: how much can I charge? :money_with_wings:
Imagine you have a spare apartment in Paris and you want to list in on Airbnb. However, you do not know a lot about Paris real estate prices, so that is a problem! If you charge too much, you will get less bookings, if you charge too little, you will have less profit! Luckily, you can call your friends *data engineer*, *data scientist* and *ML engineer* to help you out.  

They built the whole pipeline for you from scratch, from data collection all the way to model deployment. In the end they made you a nice web app, where you can input the characteristics of your apartment and you get the suggested price. :star_struck:	

That's not all! They were also kind enough to write instructions for you, so you can run it yourself:

### 1. Data engineer
As data engineers our task in this project is to collect & store data and prepare everything for the data scientist.  
The code can be found in the [`./notebooks/01_data_engineer.ipynb`](https://github.com/valira-ai/ds-career-day-workshop/blob/main/notebooks/01_data_engineer.ipynb) notebook, however, in order to run it we first need to set up our own Postgres database.

#### Database setup
There are plenty of resources online guiding us how to set up our [PostgresSQL](https://www.postgresql.org/) database. For example we could do it [locally](https://www.codecademy.com/article/installing-and-using-postgresql-locally) or in the cloud ([AWS](https://aws.amazon.com/getting-started/hands-on/create-connect-postgresql-db/) free tier is enough for our purposes). When the server is up and running, we can connect to it and create our database. We suggest using [pgAdmin](https://www.pgadmin.org/), a GUI tool made for interacting with the Postgres database sessions. In the [`./sql/`](https://github.com/valira-ai/ds-career-day-workshop/tree/main/sql) folder we can find SQL scripts that will set up the database tables, stored procedures and views for us and voilà! We are ready to run the notebook and pass the torch on to the data scientist.

