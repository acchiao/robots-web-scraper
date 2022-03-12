FROM python:latest

RUN mkdir -p /usr/src/rws
WORKDIR /usr/src/rws
COPY . /usr/src/rws

RUN pip install tqdm requests

CMD [ "python", "./main.py" ]
