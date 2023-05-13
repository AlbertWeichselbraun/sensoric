from abc import abstractmethod


class Sensor:
    skip: int = 1
    required_attributes: tuple = tuple()
    measurement_name: str
    sensor_tags: str

    @abstractmethod
    def get_sensor_fields(self):
        pass

    def check_configuration(self, configuration: dict):
        """
        Ensure that all required configuration options are set.
        """
        for attribute in self.required_attributes:
            if attribute not in configuration:
                raise ValueError(f'ConfigurationError: Configuration for module {self.__class__.__name} is missing '
                                 f'required attribute {self.__class__.__name__}.{attribute}')

