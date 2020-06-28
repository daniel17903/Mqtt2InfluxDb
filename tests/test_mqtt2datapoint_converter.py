import unittest

from mqtt2influxdb.mqtt2datapoint_converter import Mqtt2DataPointConverter

config = {
    "topicDbMapping": [
        {
            "topic": "level1/level2",
            "database": "database1",
            "measurement": "measurement",
            "tags": {
                "topictag": "<topic>",
                "datatag": "<tagdata>",
                "datatagnumeric": "<tagdatanumeric>",
                "tag": "tag"
            },
            "fields": {
                "topicfield": "<topic>",
                "datafield": "<fielddata>",
                "datafieldnumeric": "<fielddatanumeric>",
                "field": "field"
            }
        },
        {
            "topic": "level1/+",
            "database": "database2",
            "measurement": "measurement",
            "tags": {
                "topictag": "<topic>",
                "datatag": "<tagdata>",
                "datatagnumeric": "<tagdatanumeric>",
                "tag": "tag"
            },
            "fields": {
                "topicfield": "<topic>",
                "datafield": "<fielddata>",
                "datafieldnumeric": "<fielddatanumeric>",
                "field": "field"
            }
        }
    ]
}

json_data = {
    "tagdata": "tagdatafromjson",
    "tagdatanumeric": 1,
    "fielddata": "fielddatafromjson",
    "fielddatanumeric": 2
}

expected_datapoints = {
    "database1": [
        {
            "measurement": "measurement",
            "tags": {
                "topictag": "level2",
                "datatag": "tagdatafromjson",
                "datatagnumeric": 1,
                "tag": "tag"
            },
            "fields": {
                "topicfield": "level2",
                "datafield": "fielddatafromjson",
                "datafieldnumeric": 2,
                "field": "field"
            }
        }
    ],
    "database2": [
        {
            "measurement": "measurement",
            "tags": {
                "topictag": "level2",
                "datatag": "tagdatafromjson",
                "datatagnumeric": 1,
                "tag": "tag"
            },
            "fields": {
                "topicfield": "level2",
                "datafield": "fielddatafromjson",
                "datafieldnumeric": 2,
                "field": "field"
            }
        }
    ]
}

class TestMqtt2DataPointConverter(unittest.TestCase):

    def setUp(self):
        self.mqtt2dataPointConverter = Mqtt2DataPointConverter(config)
        self.maxDiff = None

    def test_convert_data_with_mapping_to_datapoints(self):
        datapoints = Mqtt2DataPointConverter(config) \
            .for_topic("level1/level2") \
            .with_json_data(json_data) \
            .create_datapoint_db_mappings()

        self.assertDictEqual(datapoints, expected_datapoints)

    def test_convert_data_with_mapping_to_datapoints_multiple_times(self):
        Mqtt2DataPointConverter(config) \
            .for_topic("level1/level2") \
            .with_json_data(json_data) \
            .create_datapoint_db_mappings()

        datapoints = Mqtt2DataPointConverter(config) \
            .for_topic("level1/level2") \
            .with_json_data(json_data) \
            .create_datapoint_db_mappings()

        self.assertDictEqual(datapoints, expected_datapoints)

    def test_ignore_other_topic(self):
        datapoints = Mqtt2DataPointConverter(config) \
            .for_topic("level1/level2/level3") \
            .with_json_data(json_data) \
            .create_datapoint_db_mappings()

        self.assertDictEqual(datapoints, {})

    def test_ignore_other_message(self):
        datapoints = Mqtt2DataPointConverter(config) \
            .for_topic("level1/level2") \
            .with_json_data({
                "wgweg": "wsegweg"
            }) \
            .create_datapoint_db_mappings()

        self.assertDictEqual(datapoints, {})


if __name__ == '__main__':
    unittest.main()
