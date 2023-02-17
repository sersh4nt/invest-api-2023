FROM python:3.11.2-slim-bullseye

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends build-essential gcc

RUN pip install --upgrade pip
RUN pip install wheel

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN mkdir -p static

EXPOSE 8000
EXPOSE 9000