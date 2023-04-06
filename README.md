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
