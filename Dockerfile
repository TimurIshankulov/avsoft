FROM python:3.10-bullseye

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
