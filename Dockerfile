FROM python:3.7.5-slim-stretch

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install wait-for-it
COPY . ./
