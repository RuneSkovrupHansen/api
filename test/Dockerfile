FROM ubuntu:latest
WORKDIR /usr/local/flask_restful
COPY . .
RUN apt-get update && apt install -y python3-pip && apt install -y curl && apt install -y iputils-ping
RUN pip install -r requirements.txt
