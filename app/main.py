from typing import Union

from fastapi import FastAPI, UploadFile
from PIL import Image
import io

app = FastAPI()


@app.get("/healthz")
def read_healthz():
    return "ok"


@app.post("/predict")
def predict(img_file: UploadFile):
    contents = img_file.file.read()
    image = Image.open(io.BytesIO(contents))
    
    return "all ok"
