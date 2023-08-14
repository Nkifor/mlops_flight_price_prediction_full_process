FROM python:3.8.17-slim-buster
LABEL maintainer="Nkifor"

WORKDIR /app
COPY . /app

RUN apt update - && apt install awscli -y

RUN pip install -r requirements.txt
RUN dvc pull
CMD ["python3", "app.py"]