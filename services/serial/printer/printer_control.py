from app.event.event import Event
from app.service.abstract_service import AbstractService
from services.serial.cnc_interface import CncInterface
from services.serial.models.cnc_status import CncStatus
from services.serial.printer.deserializers.position_deserializer import PositionDeserializer
from services.serial.serial_connection import SerialConnection
from time import sleep

import threading


class PrinterControl (AbstractService, CncInterface, Event):

    def __init__(self, servie_container):
        super().__init__(servie_container)

        self._cnc_status: CncStatus = self._get_service('cnc_status')
        self._cnc_status.connect_event('status_change', self._change_status)

        self._serial: SerialConnection = self._get_service('serial_connection')
        self._serial.connect_event('read', self._serial_read)

        self._position_deserializer = PositionDeserializer(self._cnc_status)

        self._events = {
            'info': [],
            'console': [],
            'before_idle': [],
            'before_run': [],
            'before_hold': [],
            'before_home': [],
            'before_jog': [],
            'after_idle': [],
            'after_run': [],
            'after_hold': [],
            'after_home': [],
            'after_jog': [],
            'run_end': []
        }

        self._active = False

        # self._position_flag = False
        self._status_flag = False

    def home(self):
        self.send_command('G28')
        return self

    def send_command(self, command):
        self._serial.send_line(command)
        self._run_event('console', arguments=(command + '\n',))
        return self

    def set_active(self, value):
        self._active = value
        if value:
            self._activate()
        return self

    def jog(self, movement, speed=2000):
        command = 'G0' + str(movement) + 'F' + str(speed)
        self._serial.send_line(command)
        self._run_event('console', arguments=('Jog: ' + command + '\n',))
        return self

    def set_gcode(self, gcode):
        return self

    def set_selected_line(self, line):
        return self

    def run_code(self):
        return self

    def pause(self):
        return self

    def stop(self):
        return self

    def send_bytes(self, bytes_data):
        return self

    def set_null(self, x=None, y=None, z=None, a=None, b=None):
        return self

    def _activate(self):
        self.send_command('G91')
        thread = threading.Thread(target=self._check_status)
        thread.start()

    def _check_status(self):
        self._status_flag = False
        sleep(0.1)
        self._serial.send_line('M114')
        while self._active:
            sleep(0.3)
            if self._status_flag:
                self._serial.send_line('M114')
                self._status_flag = False

    def _serial_read(self, data):
        if len(data) == 0 or not self._active:
            return
        if data[0] == 'o':
            return
        if data[0] == 'X':
            self._position_deserializer.deserialize(data)
            self._run_event('info')
            return
        self._cnc_status.set_status(data)
        self._run_event('info')
        self._status_flag = True
        print('data: ' + data)

    def _change_status(self, new_status, old_status):
        print('status change')
