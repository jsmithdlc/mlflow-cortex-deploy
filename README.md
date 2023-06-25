# Machine Learning Pipeline

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![mlflow 2.4.1](https://img.shields.io/badge/mlflow-2.4.1-lightblue.svg)](https://mlflow.org/docs/2.4.1/index.html)
[![pytorch 1.12.1](https://img.shields.io/badge/pytorch-1.12-red.svg)](https://pytorch.org/docs/1.12/)

This repository is meant as a reference guide to deploy and manage production machine learning workloads in a simple manner, by using two cool frameworks [MlFlow](https://mlflow.org/docs/latest/index.html) and [Cortex](https://docs.cortexlabs.com/).

- [Machine Learning Pipeline](#machine-learning-pipeline)
  - [MlFlow Setup](#mlflow-setup)
    - [Local](#local)
    - [Server](#server)
  - [FashionMNIST Classifier Experiment Tracking](#fashionmnist-classifier-experiment-tracking)
  - [API to serve requests with trained model](#api-to-serve-requests-with-trained-model)

This project was developed using Python 3.10. Install dependencies by running:

```bash
pip install -r requirements.txt
```

## MlFlow Setup

Configure experiment tracking & model registry locally or through an EC2 instance in AWS. Head to [https://mlflow.org/docs/latest/tracking.html](https://mlflow.org/docs/latest/tracking.html) for more details.

### Local

Run this command in the root of this project. This will launch mlflow in your machine and serve it through port 5000 by default.

```bash
mlflow ui
```

You can access the mlflow interface by going to [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser.

### Server

This part guides you through setting up mlflow in an AWS EC2 instance with S3 as an artifact store and a sqlite as a backend store. First, you should follow these steps:

1. Create an S3 bucket to use as an artifact store. This is where the model registry will reside as well as other experiment artifacts logged into mlflow.
2. [Launch an EC2 instance](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html). Upon creation, **attach an IAM role that grants your instance access to the S3 bucket** you've created in the previous step. Also, copy and paste the user data from [mlflow_user_data](mlflow_user_data.sh)
3. Edit your security group inbound rules to allow access to the instance from your IP through ssh (port 22) and HTTP (port 80). If there are problems connecting, check this [troubleshoot guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/TroubleshootingInstancesConnecting.html)
4. Connect to your instance through ssh.
5. Configure a password for your server by running the following command, replacing *testuser* with your desired username.
  
```bash
sudo htpasswd -c /etc/nginx/.htpasswd testuser
```

6. Now configure routing to the mlflow server by changing the nginx config. Open `/etc/nginx/nginx.conf` with nano or your favourite editor and insert the following code inside the "server" section of the configuration.
   
```conf
location / {
  proxy_pass http://localhost:5000/;
  auth_basic 'Restricted Content';
  auth_basic_user_file /etc/nginx/.htpasswd;
}
```

7. Start tmux shell by running `tmux`

8. Start nginx and the mlflow server.

```bash
sudo service nginx start
# install mlflow
pip3 install mlflow
# start mlflow
mlflow server \
  --backend-store-uri file:<path/to/mlruns> \
  --artifacts-destination s3://<bucket_name> \
  --host 0.0.0.0
```

1. After setting this up, you can connect to MlFlow using the instance public ip adress (dont use https as this is not configured) and entering the credentials you've defined in the nginx config. You can use `Ctrl+B+D` to dettach from your tmux shell, so you can safely logout from the instance and `tmux attach` to reattach to your shell.

## FashionMNIST Classifier Experiment Tracking

Once mlflow has been setup, you can log metrics, configuration files and, perhaps most importantly, your models into mlflow. But first, you'll need to configure some environment variables.

Copy [env.template](env.template) into a *.env* file at the root of this project and define the variables according to your mlflow deployment (local or server).

Then you can run `python train.py`. This will train a simple neural network classifier over the Fashion MNIST dataset and log into mlflow the following:

- Parameters such as learning rate, batch size and number of epochs via the `mlflow.log_params` method.
- Metrics such as loss values and accuracy across training via the `mlflow.log_metrics` method
- Pytorch trained model weights and files via the `mlflow.log_model` method.

You can explore how the experiment progresses in real time through your mlflow ui.

## API to serve requests with trained model

FastAPI and Docker are used to package the trained model for requesting inferences in a REST manner.

As in the [Track Experiments](#track-experiments) section, you'll first need to set some environment variables inside a *.env* file within the src/ directory. Create this file by using the [template](src/.env.template) as base.

The FastAPI code is defined within [src/app/main.py](src/app/main.py). It fetches a fashion-classifier model registered in mlflow and responds to requests in the /predict path. You can inspect it to understand more.

Inside src/, you'll also find a *Dockerfile* that packages the api and launches your api server in [http://127.0.0.1:80](http://127.0.0.1:80). Run it with the following command

```bash
./run_docker.sh
```

Test the api with a sample image:

```bash
python test_local_api.py --img_path dress.png
```
