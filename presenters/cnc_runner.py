from app.gui.gtk.gtk_gcode_input import GtkGCodeInput
from app.gui.gtk.interfaces.Scrool import Scroll
from app.gui.gtk.interfaces.text_view import TextView
from app.service.abstract_presenter import AbstractPresenter
from gui.inputs.gcode_input import GCodeInput
from services.gcode.gcode_file_list import GCodeFileList
from services.gcode.gcode_list import GCodeList

from services.serial.cnc_interface import CncInterface
from services.serial.cnc_selector import CncSelector


class CncRunner (AbstractPresenter):

    def __init__(self, servie_container):
        super().__init__(servie_container)
        self._gcode_file_list: GCodeFileList = self._get_service('gcode_file_list')
        self._gcode_input: GCodeInput = self._get_service('gcode_input')

        self._cnc_selector: CncSelector = self._get_service('cnc_selector')
        self._cnc_selector.connect_event('connect', self.connect)
        self._cnc_selector.connect_event('disconnect', self.disconnect)
        self._cnc_selector.connect_runner_event('console', self.print_to_console)
        self._cnc_selector.connect_runner_event('run_end', self.run_end)

        self._cnc_console: TextView or None = None
        self._cnc_runner: CncInterface or None = None
        self._console_scroll: Scroll or None = None

        self._signals = {
            'control_play': self.run_code,
            'control_pause': self.pause_code,
            'control_stop': self.stop_code,
            'control_unlock': self.unlock,
            'send_gcode': self.open_gcode_input
        }

        self._selected_code = None

    def start(self):
        self._cnc_console: TextView = self._get_gui_item('main', 'cnc_console')
        self._console_scroll: Scroll = self._get_gui_item('main', 'console_scroll')

    def open_gcode_input(self, button):
        self._gcode_input.show(self.send_gcode)

    def send_gcode(self, gcode):
        print(gcode)

    def print_to_console(self, line):
        self._cnc_console.add_line(line)
        self._console_scroll.scroll_to_bottom()

    def run_code(self, button):
        self._selected_code: GCodeList = self._gcode_file_list.get_selected_code()
        if self._selected_code:
            self._group_sensitive('control', False)
            self._group_sensitive('stop_pause', True)
            self._cnc_runner.set_gcode(self._selected_code).set_selected_line(0).run_code()

    def pause_code(self, button):
        self._cnc_runner.pause()
        self._group_sensitive('stop_pause', True)

    def stop_code(self, button):
        self._cnc_runner.stop()
        self._group_sensitive('control', True)

    def unlock(self, button):
        self._cnc_runner.send_command('$X')

    def connect(self, runner):
        self._cnc_runner = runner
        self._group_sensitive('control', True)

    def disconnect(self):
        self._group_sensitive('control', False)

    def run_end(self):
        self._group_sensitive('control', True)
