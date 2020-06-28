import paho.mqtt.client as mqtt
import json
import logging


class MqttClient:

    def __init__(self, config):
        self.config = config
        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.subscribed_topics = set()

    def _on_connect(self, client, userdata, flags, rc):
        logging.debug("MqttClient connected with result code %s" % str(rc))

        for mapping in self.config["topicDbMapping"]:
            if mapping["topic"] not in self.subscribed_topics:
                self.client.subscribe(mapping["topic"])
                self.subscribed_topics.add(mapping["topic"])
                logging.debug("subscribed to topic %s" % mapping["topic"])

    def _on_message(self, client, userdata, msg):
        topic = msg.topic
        json_data = json.loads(str(msg.payload.decode("utf-8")))
        logging.debug("received message %s on topic %s" % (json.dumps(json_data), topic))

        if "on_message_callback" in dir(self):
            self.on_message_callback(topic, json_data)

    def on_message_callback(self, callback):
        self.on_message_callback = callback

    def start(self):
        self.client.connect(self.config["mqttConnection"]["server"], self.config["mqttConnection"]["port"], 60)
        self.client.loop_forever()

    def stop(self):
        self.client.loop_stop()
