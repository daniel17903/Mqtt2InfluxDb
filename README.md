# Mqtt2InfluxDb
Writes JSON data from MQTT to InfluxDb

## Run

Adapt config.json, then

```
pip -r requirements.txt
python mqtt2influxdb/main.py
```

Or using Docker

```
docker build -t mqtt2influxdb .
docker run --name mqtt2influxdb mqtt2influxdb
```
