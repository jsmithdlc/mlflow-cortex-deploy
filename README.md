# Machine Learning Pipeline

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![mlflow 2.4.1](https://img.shields.io/badge/mlflow-2.4.1-lightblue.svg)](https://mlflow.org/docs/2.4.1/index.html)

This repository is meant as a reference guide to deploy and manage production machine learning workloads in a simple manner, by using two cool frameworks [MlFlow](https://mlflow.org/docs/latest/index.html) and [Cortex](https://docs.cortexlabs.com/).

- [Machine Learning Pipeline](#machine-learning-pipeline)
  - [MlFlow Setup](#mlflow-setup)
    - [Local](#local)
    - [Server](#server)
  - [Tracking Experiments](#tracking-experiments)

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
2. [Launch an EC2 instance](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html). Upon creation, attach an IAM role that grants your instance access to the S3 bucket you've created in the previous step. Also, copy and paste the user data from [mlflow_user_data](mlflow_user_data.sh)
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

7. Start nginx and the mlflow server.

```bash
sudo service nginx start
mlflow server \
  --backend-store-uri file:///path/to/mlruns \
  --artifacts-destination s3://bucket_name \
  --host 0.0.0.0
```

8. After setting this up, you can connect to MlFlow using the instance public ip adress and entering the credentials you've defined in the nginx config.

## Tracking Experiments

Once mlflow has been setup, you can log metrics, configuration files and, perhaps most importantly, your models into mlflow. But first, you'll need to configure some environment variables.

Copy [env.template](env.template) into a *.env* file at the root of this project and define the variables according to your mlflow deployment.

