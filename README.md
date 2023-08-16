## MLOPS Flight Price Prediction - Full Process

![Screenshot](static/proj_demo.PNG)

[Link to prediction](http://18.193.69.101:8080/predict)

## Description and shortened context of the training data

The project involves taking data, analyzing it, processing it to ultimately apply the chosen machine learning model to indicate price of flight based on given factors and then deploying the model on the server in the form of a web application.


### Data Collection

- Source of data: hhttps://www.kaggle.com/datasets/shubhambathwal/flight-price-prediction?select=Clean_Dataset.csv

Dataset contains information about flight booking options from the website Easemytrip for flight travel between India's top 6 metro cities. There are 300261 datapoints and 11 features in the cleaned dataset.


## Stages of the project

1. Planning desired outcome.
2. Configuration of environment setup.
3. Preparation of notebooks to EDA and experimenting with initial training approach.
4. Development of a modular files dealing with:
    - data ingestion,
    - data transformation,
5. Model evaluation with hyperparameter tunning
6. Local deployment of prediction model
7. Model compression in local environment
8. Setting Dockerfile locally for Run it on Virtual Machine EC2 with ECR after setting IAM
9. Setting Github Runner and Action for CI/CD to connect with AWS
10. Run of workflow
11. The prediction display may take about 30 seconds due to the reading of the converted model



### Commands to setup Docker on EC2:

1. sudo apt-get update -y
2. sudo apt-get upgrade
3. curl -fsSL https://get.docker.com -o get-docker.sh
4. sudo sh get-docker.sh
5. sudo usermod -aG docker ubuntu
6. newgrp docker

### Procedure to Configure EC2 as self-hosted runner:

1. Setting Runner based on Github guidlines
2. Adding shown below Github Secrets:
- AWS_ACCESS_KEY_ID=
- AWS_SECRET_ACCESS_KEY=
- AWS_REGION =
- AWS_ECR_LOGIN_URI =
- ECR_REPOSITORY_NAME =




