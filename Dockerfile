FROM python:3-alpine

COPY ./requirements.txt /requirements.txt
WORKDIR /

RUN pip install -r requirements.txt

COPY ./mqtt2influxdb/* /

CMD [ "python", "main.py" ]