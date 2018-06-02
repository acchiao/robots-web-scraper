FROM python:latest
MAINTAINER Arthur Chiao <chiaoarthur@gmail.com>

RUN mkdir -p /usr/src/rws
WORKDIR /usr/src/rws
COPY . /usr/src/rws

RUN pip install tqdm requests

CMD [ "python", "./main.py" ]
