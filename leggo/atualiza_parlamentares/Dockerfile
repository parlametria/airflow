FROM python:3.8.10-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /atualiza_parlamentares
COPY . /atualiza_parlamentares

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -e .
