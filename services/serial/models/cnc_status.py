from app.service.abstract_service import AbstractService
from app.event.event import Event
from services.serial.models.cnc_config import CncConfig
from services.serial.models.cnc_position import CncPosition


class CncStatus (AbstractService, Event):

    def __init__(self, servie_container):
        super().__init__(servie_container)

        self._events = {
            'status_change': [],
        }

        self._type = None
        self._status = None
        self._config = CncConfig()
        self._position = CncPosition()
        self._local_position = CncPosition()
        self._null_position = CncPosition()

        self._status_change_events = []

    def get_config(self):
        return self._config

    def get_position(self):
        return self._position

    def get_local_position(self):
        return self._local_position

    def get_null_position(self):
        return self._null_position

    def get_type(self):
        return self._type

    def set_type(self, cnc_type):
        self._type = cnc_type
        return self

    def get_status(self):
        return self._status

    def set_status(self, status):
        old_status = self._status
        self._status = status
        self._run_event('status_change', arguments=(status, old_status,))

    def __str__(self):
        string_var = 'Type: ' + str(self._type) + '\n'
        string_var += 'Status: ' + str(self._status) + '\n'
        string_var += 'Position: ' + str(self._position) + '\n'
        string_var += 'Local position: ' + str(self._local_position) + '\n'
        string_var += 'Null position: ' + str(self._null_position) + '\n\n'
        string_var += str(self._config)
        return string_var
