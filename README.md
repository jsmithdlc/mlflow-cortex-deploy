# MLFlow - Cortex Deployment

This repository is meant as a reference guide to deploy and manage production machine learning workloads in a simple yet effective manner, by using two cool frameworks [MlFlow](https://mlflow.org/docs/latest/index.html) and [Cortex](https://docs.cortexlabs.com/).

## Setup

This project was developed using Python 3.10, cortex-dev 0.42.1 and a conda environment for managing dependencies.

Install the cortex cli

```bash
bash -c "$(curl -sS https://raw.githubusercontent.com/cortexlabs/cortex/v0.42.1/get-cli.sh)"
# check your installation by running 
cortex version
```

Install pip dependencies, including MlFlow

```bash
pip install -r requirements.txt
```

## MlFlow setup

Scenario 5: MLflow Tracking Server enabled with proxied artifact storage access

### Local

```bash
mlflow ui
```

### Server

```bash
sudo yum install python3.10
sudo pip3 install mlflow
sudo yum install httpd-tools
sudo yum install nginx
sudo htpasswd -c /etc/nginx/.htpasswd testuser
sudo nano /etc/nginx/nginx.conf

location / {
proxy_pass http://localhost:5000/;
auth_basic “Restricted Content”;
auth_basic_user_file /etc/nginx/.htpasswd;
}

sudo service nginx start
mlflow server --host 0.0.0.0
```

```bash
mlflow server \
  --backend-store-uri file:///path/to/mlruns \
  # Artifact access is enabled through the proxy URI 'mlflow-artifacts:/',
  # giving users access to this location without having to manage credentials
  # or permissions.
  --artifacts-destination s3://bucket_name \
  --host remote_host
```