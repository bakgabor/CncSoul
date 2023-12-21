from app.gui.gtk.interfaces.button import Button
from app.gui.gtk.interfaces.combo_box_text import ComboBoxText
from app.gui.gtk.interfaces.label import Label
from app.gui.gtk.interfaces.list_box import ListBox
from app.service.abstract_presenter import AbstractPresenter
from gui.inputs.file_chooser import FileChooser

from services.gcode.gcode_file_list import GCodeFileList
from services.serial.cnc_interface import CncInterface
from services.serial.cnc_selector import CncSelector
from services.serial.models.cnc_position import CncPosition
from services.serial.models.cnc_status import CncStatus


class CncConnection (AbstractPresenter):

    def __init__(self, servie_container):
        super().__init__(servie_container)
        self._gcode_list = None
        self._y_label: Label or None = None
        self._z_label: Label or None = None
        self._x_label: Label or None = None

        self._cnc_selector: CncSelector = self._get_service('cnc_selector')
        self._cnc_selector.connect_event('connect', self.connect)
        self._cnc_selector.connect_event('disconnect', self.disconnect)
        self._cnc_selector.connect_runner_event('info', self._update_position)
        self._cnc_runner: CncInterface or None = None

        self._status: CncStatus = self._get_service('cnc_status')

        self._file_chooser: FileChooser = self._get_service('file_chooser')
        self._gcode_file_list: GCodeFileList = self._get_service('gcode_file_list')

        self._gcode_file_list.connect_event('change', self._update_gcode_list)

        self._file_chooser.connect_event('open', self._open_file)
        self._file_chooser.add_filters([
            {'title': 'G-code', 'pattern': ['*.ngc', '*.cnc', '*.nc', '*.tap', '*.gcode']},
            {'title': 'Text files', 'mime_types': 'text/plain'},
            {'title': 'All', 'pattern': '*'},
        ])

        self._serial_combo_box = None
        self._connect_button = None

        self._status_button: Button or None = None
        self._x_button: Button or None = None
        self._y_button: Button or None = None
        self._z_button: Button or None = None

        self._signals = {
            'serial_refresh': self.serial_refresh,
            'serial_open': self.serial_open,
            'open_gcode': self.open_gcode,
            'select_gcode': self.select_gcode
        }

    def start(self):
        self._serial_combo_box: ComboBoxText = self._get_gui_item('connect', 'connect')
        self._item_sensitive('connect', 'serial_open_button', False)
        self._connect_button: Button = self._get_gui_item('connect', 'serial_open_button')
        self._gcode_list: ListBox = self._get_gui_item('connect', 'gcode_list')

        self._status_button: Button = self._get_gui_item('main', 'status')
        self._x_button: Button = self._get_gui_item('main', 'x_button')
        self._y_button: Button = self._get_gui_item('main', 'y_button')
        self._z_button: Button = self._get_gui_item('main', 'z_button')
        self._x_label: Label = self._get_gui_item('main', 'x_label')
        self._y_label: Label = self._get_gui_item('main', 'y_label')
        self._z_label: Label = self._get_gui_item('main', 'z_label')

        self._group_sensitive('control', False)

        self.serial_refresh(None)

    def select_gcode(self, item):
        selected = self._gcode_list.get_selected()
        if selected is not None:
            self._set_window_title('Cnc Controller: ' + selected)
            self._gcode_file_list.set_selected(selected)

    def open_gcode(self, button):
        self._file_chooser.show()

    def serial_refresh(self, button):
        ports = self._cnc_selector.get_ports()
        self._serial_combo_box.new_list(ports)
        self._cnc_selector.set_port(self._serial_combo_box.get_active())
        self._item_sensitive('connect', 'serial_open_button', self._serial_combo_box.get_active() is not None)

    def serial_open(self, button):
        if self._cnc_selector.is_connected():
            self._cnc_selector.disconnect()
            self._connect_button.set_label('Open')
            return
        self._cnc_selector.connect()
        self._connect_button.set_label('Disconnect')

    def connect(self, runner):
        self._cnc_runner = runner
        self._group_sensitive('control', True)

    def disconnect(self):
        self._group_sensitive('control', False)

    def _update_position(self):
        self._status_button.set_label(self._status.get_status())
        position: CncPosition = self._status.get_position()
        local_position: CncPosition = self._status.get_local_position()
        self._x_button.set_label("{:.2f}".format(local_position.get_x()))
        self._y_button.set_label("{:.2f}".format(local_position.get_y()))
        self._z_button.set_label("{:.2f}".format(local_position.get_z()))

        self._x_label.set_text("{:.2f}".format(position.get_x()))
        self._y_label.set_text("{:.2f}".format(position.get_y()))
        self._z_label.set_text("{:.2f}".format(position.get_z()))

    def _update_gcode_list(self):
        names = self._gcode_file_list.get_names()
        self._gcode_list.set_list(names)

    def _open_file(self, filename):
        self._gcode_file_list.open_file(filename)
        self._set_window_title(self._gcode_file_list.get_selected_name())

