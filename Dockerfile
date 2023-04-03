#Dockerfile
FROM python:3.9

WORKDIR /app

COPY ./models/model.joblib ./models/model.joblib
COPY ./src ./src
COPY ./requirements.txt ./requirements.txt
COPY ./setup.py ./setup.py

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
RUN pip install ./

WORKDIR ./src

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
