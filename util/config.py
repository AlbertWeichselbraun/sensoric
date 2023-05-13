from collections import defaultdict
from configparser import ConfigParser
from pathlib import Path


class SensoricConfiguration:

    def __init__(self, configuration_file: Path):
        self.config = ConfigParser()
        self.config.read(configuration_file)

    def _get_config(self, configuration_group: str) -> dict[str, dict[str, str]]:
        """
        Retrieve the configuration dictionary for the given configuration group.

        Returns:
            A dictionary with all configured items and their corresponding configuration values.
        """
        config_group = defaultdict(dict)
        for item in self.config[configuration_group]:
            if ':' not in item:
                config_group[item] = {}
                continue
            config_item, config_item_key = item.split(':')
            config_value = self.config[configuration_group][item]
            config_group[config_item][config_item_key] = [
                c.strip() for c in config_value.split(',')] if ',' in config_value else config_value
        return config_group

    def get_sensors(self):
        return self._get_config('sensors')

    def get_sink(self):
        return self._get_config('sinks')

    def batch_size(self):
        return self.config['global'].get('batch_size', 1)
