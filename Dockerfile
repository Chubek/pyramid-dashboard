FROM python:latest
WORKDIR /home/dash-fin

COPY . ./
RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone
RUN apt-get update && apt upgrade -y && apt-get install build-essential libsvm-dev ffmpeg libsm6 libxext6 -y

RUN pip install --no-cache-dir -r requirements.txt


ENTRYPOINT ["/bin/bash"]