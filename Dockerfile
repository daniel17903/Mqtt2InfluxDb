FROM python:3-alpine

COPY ./requirements.txt /requirements.txt
WORKDIR /

RUN pip install -r requirements.txt

COPY ./mqtt2influxdb /mqtt2influxdb
COPY ./config.json /config.json

CMD [ "python", "/mqtt2influxdb/main.py" ]
