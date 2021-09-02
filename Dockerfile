FROM python:latest
WORKDIR /home/dash-fin

COPY . ./

RUN apt-get update && apt-get install build-essential libsvm-dev ffmpeg libsm6 libxext6 -y

RUN pip install --no-cache-dir -r requirements.txt


