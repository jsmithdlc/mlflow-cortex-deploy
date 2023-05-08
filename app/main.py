from typing import Union
import torch
from torchvision.transforms import ToTensor
import mlflow
import numpy as np

from fastapi import FastAPI, UploadFile
from PIL import Image
import io


mlflow.set_tracking_uri("http://127.0.0.1:5000")

app = FastAPI()
model: torch.nn.Module = mlflow.pytorch.load_model(
    "runs:/ff25d15795b74f9d8a27d122b2c47fe9/mnist-model"
)
transform = ToTensor()

device = "cuda" if torch.cuda.is_available() else "cpu"

classes = [
    "T-shirt/top",
    "Trouser",
    "Pullover",
    "Dress",
    "Coat",
    "Sandal",
    "Shirt",
    "Sneaker",
    "Bag",
    "Ankle boot",
]


@app.get("/healthz")
def read_healthz():
    return "ok"


@app.post("/predict")
def predict(img_file: UploadFile):
    contents = img_file.file.read()
    image = Image.open(io.BytesIO(contents)).convert("L")
    image = image.resize((28, 28))
    model_input = transform(image)
    model_input = model_input.reshape((1, 1, 28, 28))
    model.eval()
    with torch.no_grad():
        model_input = model_input.to(device)
        pred = model(model_input)
        predicted = classes[pred[0].argmax(0)]
    return {"prediction": predicted}
