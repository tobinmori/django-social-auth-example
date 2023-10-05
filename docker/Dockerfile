# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
COPY . .
RUN python3 -m pip install pip --upgrade
RUN python3 setup.py install
RUN pip3 install -r requirements.txt

## custom Akamai backend. . .
COPY ./core/backends/aic.py /usr/local/lib/python3.8/site-packages/social_auth_core-4.1.0-py3.8.egg/social_core/backends/aic.py

ENV DJANGO_SETTINGS_MODULE="social_app.settings"

EXPOSE 8000
