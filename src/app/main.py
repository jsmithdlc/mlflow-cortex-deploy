from typing import Union
import torch
from torchvision.transforms import ToTensor
import mlflow
import numpy as np

from fastapi import FastAPI, UploadFile
from PIL import Image
from pydantic import BaseSettings
import io
import json


class Settings(BaseSettings):
    model_stage: str
    model_name: str


device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)

settings = Settings()

# fetches last version of model in specified stage
model_path = "models:/{}/{}".format(settings.model_name, settings.model_stage)
model = mlflow.pytorch.load_model(
    model_uri=model_path,
    map_location=torch.device(device),
)

# model input shape and classes can be extracted from model info
model_info = mlflow.models.get_model_info(model_uri=model_path)
input_shape = model_info.signature.inputs.to_dict()[0]["tensor-spec"]["shape"]
output_classes = model_info.metadata["classes"]

# transforms a PIL image into a tensor.
transform = ToTensor()

app = FastAPI()


@app.get("/healthz")
def read_healthz():
    return "ok"


@app.post("/predict")
def predict(img_file: UploadFile):
    # image is read from payload and resized + reshaped to model input shape
    contents = img_file.file.read()
    image = Image.open(io.BytesIO(contents)).convert("L")
    image = image.resize([input_shape[-2], input_shape[-1]])
    model_input = transform(image)
    model_input = model_input.reshape(input_shape)
    model.eval()
    with torch.no_grad():
        model_input = model_input.to(device)
        pred = model(model_input)
        predicted = output_classes[pred[0].argmax(0)]
    return {"prediction": predicted}
