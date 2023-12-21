from app.gui.gtk.gtk_gcode_input import GtkGCodeInput
from app.service.abstract_service import AbstractService


class GCodeInput (AbstractService):

    def __init__(self, servie_container):
        super().__init__(servie_container)
        self._input = GtkGCodeInput()

    def show(self, function):
        self._input.show(function)
