#!/bin/bash
yum update -y
yum install python3-pip -y
pip3 install mlflow
yum install httpd-tools -y
yum install nginx -y
yum install tmux -y