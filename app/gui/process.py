from app.service.abstract_service import AbstractService


class Process (AbstractService):

    def __init__(self, servie_container):
        super().__init__(servie_container)
        self._level_bar = None

    def set_level_bar(self, level_bar):
        self._level_bar = level_bar

    def set_value(self, value):
        self._level_bar.set_value(value)
