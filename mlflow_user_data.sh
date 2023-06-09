#!/bin/bash
sudo yum update -y
sudo yum install python3-pip -y
pip3 install mlflow
sudo yum install httpd-tools -y
sudo yum install nginx -y