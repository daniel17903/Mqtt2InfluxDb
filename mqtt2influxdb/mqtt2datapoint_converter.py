from functools import reduce


class Mqtt2DataPointConverter:

    def __init__(self, config):
        self.mappings = config["topicDbMapping"]

    def _topics_match(self, topic1, topic2):
        return topic1 in [topic2, topic2.rsplit("/", 1)[0] + "/+"]

    def for_topic(self, topic):
        self.topic = topic
        self.mappings = list(filter(lambda m: self._topics_match(m["topic"], topic), self.mappings))
        return self

    def _applicable(self, mapping, json_data):
        """a mapping is applicable to json_data if the json_data contains values for all placeholders defined in the mapping"""
        placeholders = self._extract_placeholders(mapping["fields"])
        placeholders.extend(self._extract_placeholders(mapping["tags"]))
        return reduce(lambda a, b: a and (b == "topic" or b in json_data), placeholders, True)

    def _extract_placeholders(self, template):
        values_with_placeholder_in_mapping = list(
            filter(lambda v: "<" in v and v.find(">") > v.find("<"), list(template.values())))
        placeholders = list(map(lambda v: v[v.find("<") + 1:v.find(">")], values_with_placeholder_in_mapping))
        return placeholders

    def with_json_data(self, json_data):
        self.data = json_data
        self.mappings = list(filter(lambda m: self._applicable(m, json_data), self.mappings))
        return self

    def _fill_placeholders(self, template):
        placeholders = self._extract_placeholders(template)
        value_from_topic = self.topic.rsplit("/", 1)[-1]
        for key, value in template.items():
            value = str(value)
            value = value.replace("<topic>", value_from_topic)
            for placeholder in placeholders:
                if placeholder == "topic": continue
                value = value.replace("<%s>" % placeholder, str(self.data[placeholder]))

            if value.isnumeric(): value = float(value)
            template[key] = value

        return template

    def create_datapoint_db_mappings(self):
        datapoint_db_mappings = {}
        for mapping in self.mappings:
            if mapping["database"] not in datapoint_db_mappings:
                datapoint_db_mappings[mapping["database"]] = []

            datapoint_db_mappings[mapping["database"]].append({
                "measurement": mapping["measurement"],
                "tags": self._fill_placeholders(mapping["tags"].copy()),
                "fields": self._fill_placeholders(mapping["fields"].copy()),
            })

        return datapoint_db_mappings
