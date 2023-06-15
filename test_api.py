import requests
import argparse
import json

parser = argparse.ArgumentParser(description="test deployed api")
parser.add_argument("--img_path", required=True, help="path to image to predict")
args = parser.parse_args()


img_file = open(args.img_path, "rb")
response = requests.post(
    url="http://127.0.0.1:80/predict", files={"img_file": img_file}
)
output = json.loads(response.content.decode())


