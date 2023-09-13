FROM ubuntu:22.04
WORKDIR /
COPY requirements.txt /
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip install -r requirements.txt