FROM python:3.8.17-slim-buster
LABEL maintainer="Nkifor"

WORKDIR /app
COPY . /app

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY


RUN apt update - && apt install awscli -y

RUN pip install -r requirements.txt
RUN dvc remote modify -v --local myremote \
                    access_key_id $AWS_ACCESS_KEY_ID
RUN dvc remote modify -v --local myremote \
                    secret_access_key $AWS_SECRET_ACCESS_KEY
RUN dvc remote add -d storage s3://mlopsflightpricepredictionartifacts
RUN dvc pull
CMD ["python3", "app.py"]
