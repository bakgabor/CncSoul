from app.gui.gtk.gtk_set_input import GtkSetInput
from app.service.abstract_service import AbstractService


class SetInput(AbstractService):

    def __init__(self, servie_container):
        super().__init__(servie_container)
        self._input = GtkSetInput()

    def show(self, move_to, set_value):
        self._input.show(move_to, set_value)

    def connect_event(self, event, function):
        self._input.connect_event(event, function)
