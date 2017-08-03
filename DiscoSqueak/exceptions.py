class ConfigError(Exception):
    def __init__(self, message, config_option=None):
        super().__init__(message)
        self._message = message
        self._config_option = config_option

    @property
    def message(self):
        return self._message

    @property
    def config_option(self):
        return self._config_option
