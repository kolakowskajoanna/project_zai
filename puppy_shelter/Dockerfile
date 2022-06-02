FROM python:3.9.10-slim-buster
RUN apt update && apt install -y \
    build-essential libpq-dev  \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY . /app
WORKDIR /app
EXPOSE 8000
