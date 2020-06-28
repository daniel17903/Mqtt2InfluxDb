import json
import logging
import os

from influxdb_client import InfluxDbClient
from mqtt2datapoint_converter import Mqtt2DataPointConverter
from mqtt_client import MqttClient

logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))

def load_config():
    with open('../config.json') as json_file:
        return json.load(json_file)


def on_mqtt_message(topic, json_data):
    try:
        datapoints = Mqtt2DataPointConverter(config) \
            .for_topic(topic) \
            .with_json_data(json_data) \
            .create_datapoint_db_mappings()

        for database in datapoints.keys():
            influxDbClient.write_datapoints_to_database(datapoints[database], database)

    except Exception:
        logging.exception("Failed to process message on topic %s" % topic)


config = load_config()
influxDbClient = InfluxDbClient(config)

mqttClient = MqttClient(config)
mqttClient.on_message_callback(on_mqtt_message)
mqttClient.start()
