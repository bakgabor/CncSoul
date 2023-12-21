from app.gui.gui_generator import GuiGenerator
from app.gui.process import Process
from gui.inputs.file_chooser import FileChooser
from gui.inputs.gcode_input import GCodeInput
from gui.inputs.set_input import SetInput
from presenters.cnc_control import CncControl
from presenters.cnc_runner import CncRunner
from presenters.cnc_connection import CncConnection

from services.gcode.gcode_file_list import GCodeFileList
from services.serial.cnc_selector import CncSelector
from services.serial.grbl.grbl_control import GRBLControl
from services.serial.models.cnc_status import CncStatus
from services.serial.printer.printer_control import PrinterControl
from services.serial.serial_connection import SerialConnection


class Services:

    def __init__(self):
        self._services = {
            # Presenters
            'cnc_connection': CncConnection,
            'cnc_control': CncControl,
            'cnc_runner': CncRunner,

            # Services
            'gcode_input': GCodeInput,
            'set_input': SetInput,
            'gui_generator': GuiGenerator,
            'process': Process,
            'serial_connection': SerialConnection,

            # Controllers
            'grbl_control': GRBLControl,
            'printer_control': PrinterControl,

            'cnc_selector': CncSelector,
            'cnc_status': CncStatus,

            'file_chooser': FileChooser,
            'gcode_file_list': GCodeFileList,
        }
