FROM ubuntu:latest
WORKDIR /usr/local/flaks_restful
COPY . .
RUN apt-get update && apt-get install -y python3-pip
RUN pip install -r requirements.txt
