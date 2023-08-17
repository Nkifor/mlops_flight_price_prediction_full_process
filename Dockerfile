FROM python:3.8.17-slim-buster
LABEL maintainer="Nkifor"



RUN apt update -y && apt install awscli -y
RUN apt-get install -y --no-install-recommends \
        libatlas-base-dev gfortran nginx supervisor

RUN pip3 install uwsgi
COPY ./requirements.txt /project/requirements.txt

RUN pip3 install -r /project/requirements.txt

RUN useradd --no-create-home nginx

RUN rm /etc/nginx/sites-enabled/default
RUN rm -r /root/.cache

COPY nginx.conf /etc/nginx/
COPY flask-site-nginx.conf /etc/nginx/conf.d/
COPY uwsgi.ini /etc/uwsgi/
COPY supervisord.conf /etc/

COPY /app /project

WORKDIR /project

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 unzip -y
#&& pip install -r requirements.txt
CMD ["/usr/bin/supervisord"]