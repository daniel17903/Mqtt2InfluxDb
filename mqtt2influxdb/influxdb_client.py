from influxdb import InfluxDBClient
import logging


class InfluxDbClient:

    def __init__(self, config):
        self.client = InfluxDBClient(config["influxDbConnection"]["server"], config["influxDbConnection"]["port"],
                                     config["influxDbConnection"]["user"], config["influxDbConnection"]["password"])

    def write_datapoints_to_database(self, datapoints, database):
        self.client.create_database(database)
        self.client.switch_database(database)
        self.client.write_points(datapoints)
        logging.debug("wrote %s into database %s" % (datapoints, database))
