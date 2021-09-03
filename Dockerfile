FROM ubuntu:latest
WORKDIR /home/dash-fin

COPY . ./
RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone
RUN apt-get update && apt upgrade && apt-get install build-essential  libsvm-dev ffmpeg libsm6 zlib1g-dev libncurses5-dev libssl-dev libsqlite3-dev libxext6 libreadline-gplv2-dev libncursesw5-dev wget -y

RUN pip install --no-cache-dir -r requirements.txt


