FROM python:3.12.1

ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app

RUN apt-get update && apt-get install -y default-libmysqlclient-dev libssl-dev && apt install -y default-mysql-client
RUN apt-get update && apt-get install -y pkg-config
