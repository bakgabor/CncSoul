
class CncConfig:

    def __init__(self, configs=None, machine_configs=None):
        if configs is None:
            configs = {}
        if machine_configs is None:
            machine_configs = {}
        self._configs = configs
        self._machine_configs = machine_configs

    def add_machine_config(self, key, data):
        self._machine_configs[key] = data
        return self

    def get_machine_config(self, key):
        return self._machine_configs[key]

    def add(self, key, data):
        self._configs[key] = data
        return self

    def get(self, key):
        if key in self._configs:
            return self._configs[key]
        return None

    def clear(self):
        self._configs = {}
        self._machine_configs = {}
        return self

    def __str__(self):
        configs = 'config: \n'
        for key, value in self._configs.items():
            configs += '    ' + key + ': ' + value + '\n'
        configs += '\nmachine configs: \n'
        for key, value in self._machine_configs.items():
            configs += '     ' + key + ': ' + value + '\n'
        return configs
