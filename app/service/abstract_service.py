
class AbstractService:

    def __init__(self, servie_container):
        self._servie_container = servie_container

    def _get_container(self):
        return self._servie_container

    def _get_service(self, key):
        return self._servie_container.get(key)
