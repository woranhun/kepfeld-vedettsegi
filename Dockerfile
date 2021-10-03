# syntax=docker/dockerfile:1

FROM python:3.9.7

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt update ##[edited]
RUN apt install ffmpeg libsm6 libxext6 -y

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "main.py" ]