import requests
from PIL import Image
import os
import json

base_url = "http://127.0.0.1:8000/"
img_path = "./app/condor.jpg"

payload = {
    "img_file": open(img_path, "rb"),
    "content type": "image/jpeg",
    "filename": os.path.basename(img_path),
}

try:
    r = requests.post(url=os.path.join(base_url, "predict"), files=payload)
    print(json.loads(r.content))
except:
    print("not worked")