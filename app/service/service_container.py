from config.services import Services


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ServiceContainer(Services, metaclass=SingletonMeta):

    def __init__(self):
        self._innit_services = {}
        super().__init__()

    def get(self, key):
        if key in self._innit_services:
            return self._innit_services[key]
        service = self._services[key](self)
        self._innit_services[key] = service
        return service
