from app.gui.gtk.interfaces.label import Label
from app.service.abstract_presenter import AbstractPresenter
from gui.inputs.set_input import SetInput
from services.serial.cnc_interface import CncInterface
from services.serial.cnc_selector import CncSelector


class CncControl (AbstractPresenter):

    def __init__(self, servie_container):
        super().__init__(servie_container)
        self._movement_label = None
        self._signals = {
            'move_up': self.move_up,
            'move_down': self.move_down,
            'move_forward': self.move_forward,
            'move_back': self.move_back,
            'move_left': self.move_left,
            'move_right': self.move_right,
            'change_x': self.change_x,
            'change_y': self.change_y,
            'change_z': self.change_z,
            'set_null_x': self.set_null_x,
            'set_null_y': self.set_null_y,
            'set_null_z': self.set_null_z,
            'select_movement': self.select_movement,
            'set_null_xyz': self.set_null_xyz,
            'move_forward_left': self.move_forward_left,
            'move_forward_right': self.move_forward_right,
            'move_back_left': self.move_back_left,
            'move_back_right': self.move_back_right,
            'home': self.home
        }

        self._cnc_selector: CncSelector = self._get_service('cnc_selector')
        self._cnc_selector.connect_event('connect', self.connect)
        self._cnc_selector.connect_event('disconnect', self.disconnect)
        self._cnc_runner: CncInterface or None = None

        self._set_input: SetInput = self._get_service('set_input')
        self._set_input.connect_event('destroy', self._reset_change_pos)

        self._change_pos = None

        self._movements = {
            0: 0.001,
            1: 0.005,
            2: 0.01,
            3: 0.05,
            4: 0.1,
            5: 0.5,
            6: 1,
            7: 5,
            8: 10,
            9: 50,
            10: 100,
            11: 200
        }
        self._movement = 1

    def start(self):
        self._movement_label: Label = self._get_gui_item('main', 'movement_label')

    def home(self, button):
        self._cnc_runner.home()

    def select_movement(self, object):
        value = round(object.get_value())
        object.set_value(value)
        self._movement = self._movements[value]
        self._movement_label.set_text(str(self._movements[value]))

    def change_x(self, button):
        if self._change_pos is None:
            self._change_pos = 'X'
            self._set_input.show(self._go_to_position, self._set_position)

    def change_y(self, button):
        if self._change_pos is None:
            self._change_pos = 'Y'
            self._set_input.show(self._go_to_position, self._set_position)

    def change_z(self, button):
        if self._change_pos is None:
            self._change_pos = 'Z'
            self._set_input.show(self._go_to_position, self._set_position)

    def set_null_xyz(self, button):
        self._cnc_runner.set_null(x=0, y=0, z=0)

    def set_null_x(self, button):
        self._cnc_runner.set_null(x=0)

    def set_null_y(self, button):
        self._cnc_runner.set_null(y=0)

    def set_null_z(self, button):
        self._cnc_runner.set_null(z=0)

    def move_up(self, button):
        self._cnc_runner.jog('Z' + str(self._movement), 2000)

    def move_down(self, button):
        self._cnc_runner.jog('Z-' + str(self._movement), 2000)

    def move_forward(self, button):
        self._cnc_runner.jog('Y' + str(self._movement), 2000)

    def move_back(self, button):
        self._cnc_runner.jog('Y-' + str(self._movement), 2000)

    def move_forward_left(self, button):
        self._cnc_runner.jog('Y' + str(self._movement) + 'X-' + str(self._movement), 2000)

    def move_forward_right(self, button):
        self._cnc_runner.jog('Y' + str(self._movement) + 'X' + str(self._movement), 2000)

    def move_back_left(self, button):
        self._cnc_runner.jog('Y-' + str(self._movement) + 'X-' + str(self._movement), 2000)

    def move_back_right(self, button):
        self._cnc_runner.jog('Y-' + str(self._movement) + 'X' + str(self._movement), 2000)

    def move_left(self, button):
        self._cnc_runner.jog('X-' + str(self._movement), 2000)

    def move_right(self, button):
        self._cnc_runner.jog('X' + str(self._movement), 2000)

    def _go_to_position(self, pos):
        self._cnc_runner.jog(self._change_pos + pos, 2000)
        self._change_pos = None

    def _set_position(self, pos):
        if self._change_pos == "X":
            self._cnc_runner.set_null(x=int(pos))
        if self._change_pos == "Y":
            self._cnc_runner.set_null(y=int(pos))
        if self._change_pos == "Z":
            self._cnc_runner.set_null(z=int(pos))
        self._change_pos = None

    def _reset_change_pos(self):
        self._change_pos = None

    def connect(self, runner):
        self._cnc_runner = runner
        self._group_sensitive('control', True)

    def disconnect(self):
        self._group_sensitive('control', False)
