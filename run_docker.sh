#!/bin/bash
cd src
docker build -t fashion-mlflow:latest .
docker run --name mlflow-fastapi --rm --network="host" --env-file=.env fashion-mlflow