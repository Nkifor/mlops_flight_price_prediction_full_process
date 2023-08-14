FROM python:3.8.17-slim-buster
LABEL maintainer="Nkifor"

WORKDIR /app
COPY . /app

COPY  https://flightpredictioncredentials.s3.eu-central-1.amazonaws.com/.aws/credentials.txt /app/.aws/credentials.txt




ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ENV AWS_ACCESS_KEY_ID=credentials.access_key
ENV AWS_SECRET_ACCESS_KEY=credentials.secret_key


RUN apt update - && apt install awscli -y


RUN pip install -r requirements.txt
RUN wget https://flightpredictioncredentials.s3.eu-central-1.amazonaws.com/.aws/credentials.txt
RUN session = boto3.Session(profile_name='flightpred')
RUN credentials = session.get_credentials()
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ENV AWS_ACCESS_KEY_ID=credentials.access_key
ENV AWS_SECRET_ACCESS_KEY=credentials.secret_key


RUN dvc remote modify --local myremote \
                    access_key_id ${AWS_ACCESS_KEY_ID}
RUN dvc remote modify --local myremote \
                    secret_access_key ${AWS_SECRET_ACCESS_KEY}
RUN dvc remote add -d storage s3://mlopsflightpricepredictionartifacts
RUN dvc pull
CMD ["python3", "app.py"]
