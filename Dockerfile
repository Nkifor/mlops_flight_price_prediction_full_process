FROM python:3.8.17-slim-buster
LABEL maintainer="Nkifor"

WORKDIR /app
COPY . /app


RUN apt update - && apt install awscli -y


RUN pip install -r requirements.txt

RUN wget https://flightpredictioncredentials.s3.eu-central-1.amazonaws.com/.aws/credentials.txt -O /tmp/credentials.txt
RUN mkdir -p /app/.aws && python3 -c "import configparser; config = configparser.ConfigParser(); config.read('/tmp/credentials.txt'); print(f'AWS_ACCESS_KEY_ID={config['username']['aws_access_key_id']}'); print(f'AWS_SECRET_ACCESS_KEY={config['username']['aws_secret_access_key']}')" > /app/.aws/credentials


RUN dvc remote modify --local myremote \
                    access_key_id ${AWS_ACCESS_KEY_ID}
RUN dvc remote modify --local myremote \
                    secret_access_key ${AWS_SECRET_ACCESS_KEY}
RUN dvc remote add -d storage s3://mlopsflightpricepredictionartifacts
RUN dvc pull
CMD ["python3", "app.py"]
