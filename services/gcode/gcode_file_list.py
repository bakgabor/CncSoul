from app.service.abstract_service import AbstractService
from app.event.event import Event
from services.gcode.builder.gcode_file_loader import GCodeFileLoader
from services.gcode.gcode_list import GCodeList


def _get_filename(route):
    route_array = route.split("/")
    return route_array[len(route_array) - 1]


class GCodeFileList (AbstractService, Event):

    def __init__(self, servie_container):
        super().__init__(servie_container)
        self._events = {
            'change': []
        }
        self._codes = {}
        self._selected = None

    def open_file(self, file):
        code = GCodeList(
            codes=[
                GCodeFileLoader(file)
            ],
        )
        file_name = _get_filename(file)
        self._codes[file_name] = code
        self._run_event('change')
        if self._selected is None:
            self._selected = file_name

    def set_selected_line(self, line):
        if self._selected is not None:
            return self._codes[self._selected].set_selected_line(line)

    def get_names(self):
        return self._codes.keys()

    def set_selected(self, name):
        self._selected = name

    def get_selected_name(self):
        return self._selected

    def get_selected_code(self):
        if self._selected is not None:
            return self._codes[self._selected]
        return None

    def get_code(self, name):
        return self._codes[name]
