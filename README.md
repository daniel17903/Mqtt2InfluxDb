
# Mqtt2InfluxDb
Writes JSON data from MQTT to InfluxDb

## Configuration

The configuration is stored in the `config.json` file. An example configuration looks like this:

    {
      "mqttConnection": {
        "server": "192.168.178.50",
        "port": 1883,
        "user": "",
        "password": ""
      },
      "influxDbConnection": {
        "server": "192.168.178.50",
        "port": 8086,
        "user": "",
        "password": ""
      },
      "topicDbMapping": [
        {
          "topic": "level1/level2",
          "database": "databaseName",
          "measurement": "measurementName",
          "tags": {
            "tag1": "tag1"
          },
          "fields": {
            "field1": "field1",
            "field2": "field2"
          }
        },
        {
          "topic": "level1/+",
          "database": "linkquality",
          "measurement": "linkquality",
          "tags": {
            "device": "<topic>"
          },
          "fields": {
            "linkquality": "<linkquality>"
          }
        }
      ]
    }

### TopicDbMapping
Configures which MQTT topics should be subscribed and the data that should be written to InfluxDb.
|Key|Description|
|--|--|
|topic|MQTT Topic to listen on. Can also contain wildcards like ‘+‘ or ‘#‘ (see https://mosquitto.org/man/mqtt-7.html). If a message is received on this topic, a measurement as defined in this configuration will be written to InfluxDb.|
|database|Name of an InfluxDb database to store data in when a message is received on the specified MQTT Topic|
|measurement|Name of the measurement that is written to the database|
|tags|A JSON object containing an arbitrary number of key-value pairs to be stored as the tags of this measurement. Values can contain variables like `<key>`. All variables will be replaced with data contained in the MQTT message. For example, if a message `{“key“: “value“}` is received, `<key>` will be replaced by `value`. If a MQTT message does not contain data for all variables it will be ignored. Also, the variable `<topic>` will always be replaced with the last level of the MQTT topic. For example, when subscribed to topic `level1/level2`, `<topic>` will be replaced by `level2`.|
|fields|Like tags, but for fields to be stored with this measurement.|


## Usage

```
pip -r requirements.txt
python mqtt2influxdb/main.py
```

Or using Docker

```
docker build -t mqtt2influxdb .
docker run --name mqtt2influxdb mqtt2influxdb
```
