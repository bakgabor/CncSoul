from app.service.abstract_service import AbstractService
from app.event.event import Event
from services.serial.cnc_interface import CncInterface
from services.serial.grbl.grbl_runner import GrblRunner
from services.serial.grbl.serializers.grbl_config_deserializer import GrblConfigDeserializer
from services.serial.grbl.serializers.grbl_info_deserializer import GrblInfoDeserializer
from services.serial.grbl.serializers.grbl_machine_config_deserializer import GrblMachineConfigDeserializer
from services.serial.models.cnc_position import CncPosition
from services.serial.models.cnc_status import CncStatus
from services.serial.serial_connection import SerialConnection
from time import sleep

import threading


class GRBLControl(AbstractService, CncInterface, Event):

    def __init__(self, servie_container):
        super().__init__(servie_container)

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

        self._serial: SerialConnection = self._get_service('serial_connection')
        self._cnc_status: CncStatus = self._get_service('cnc_status')
        self._cnc_status.connect_event('status_change', self._change_status)

        self._info_deserializer = GrblInfoDeserializer(self._cnc_status)
        self._config_deserializer = GrblConfigDeserializer(self._cnc_status)
        self._machine_config_deserializer = GrblMachineConfigDeserializer(self._cnc_status)

        self._serial.connect_event('read', self._serial_read)

        self._active = False
        self._status_flag = False

        self._grbl_runner = GrblRunner(self, self._cnc_status)
        self._grbl_runner.connect_event('next_command', self._next_command)
        self._grbl_runner.connect_event('synchronization_error', self._synchronization_error)
        self._grbl_runner.connect_event('run_end', self._run_end)

    def _run_end(self):
        self._run_event('run_end')
        self._run_event('console', arguments=('End\n',))

    def _synchronization_error(self):
        self._run_event('console', arguments=('Synchronization error\n',))

    def _next_command(self, gcode):
        self._run_event('console', arguments=(str(gcode),))

    def home(self):
        print('home')
        return self

    def send_command(self, command):
        self._serial.send_line(command)
        self._run_event('console', arguments=(command,))
        return self

    def set_active(self, value):
        self._active = value
        if value:
            self._activate()
        return self

    def jog(self, movement, speed=2000):
        command = '$J=G21G91' + str(movement) + 'F' + str(speed)
        self._serial.send_line(command)
        self._run_event('console', arguments=('Jog: ' + command,))
        return self

    def set_gcode(self, gcode):
        self._grbl_runner.set_gcode(gcode)
        return self

    def set_selected_line(self, line):
        self._grbl_runner.set_selected_line(line)
        return self

    def run_code(self):
        self._run_event('console', arguments=('Run\n',))
        self._grbl_runner.run_code()
        return self

    def pause(self):
        self._grbl_runner.pause()
        return self

    def stop(self):
        self._grbl_runner.stop()
        return self

    def send_bytes(self, bytes_data):
        self._serial.send_bytes(bytes_data)
        return self

    def set_null(self, x=None, y=None, z=None, a=None, b=None):
        null_position: CncPosition = self._cnc_status.get_null_position()
        position: CncPosition = self._cnc_status.get_position()
        code = 'G10L20P1'
        if x is not None:
            code += 'X' + str(x)
            null_position.set_x(position.get_x() - x)
        if y is not None:
            code += 'Y' + str(y)
            null_position.set_y(position.get_y() - y)
        if z is not None:
            code += 'Z' + str(z)
            null_position.set_z(position.get_z() - z)
        if a is not None:
            code += 'A' + str(a)
            null_position.set_a(position.get_a() - a)
        if b is not None:
            code += 'B' + str(b)
            null_position.set_b(position.get_b() - b)
        self.send_command(code)
        return self

    def _check_status(self):
        self._status_flag = False
        sleep(0.1)
        self._serial.send_line('?')
        while self._active:
            sleep(0.3)
            if self._status_flag:
                self._serial.send_line('?')
                self._status_flag = False

    def _serial_read(self, data):
        if len(data) == 0 or not self._active:
            return
        if data[0] == '<':
            self._info_deserializer.deserialize(data)
            self._run_event('info')
            self._status_flag = True
        # if data[0] == 'o':
        #     # print('ok')
        #     return
        if data[0] == '$':
            self._machine_config_deserializer.deserialize(data)
            return
        if data[0] == 'e':
            self._run_event('console', arguments=(str(data) + '\n',))
            print(str(data))
            return
        if data[0] == '[':
            self._config_deserializer.deserialize(data)
            return

    def _activate(self):
        self._serial.send_line('$$')
        self._serial.send_line('$G')
        thread = threading.Thread(target=self._check_status)
        thread.start()

    def _change_status(self, new_status, old_status):
        if old_status:
            self._run_event('after_' + old_status.lower())
        if new_status:
            self._run_event('before_' + new_status.lower())
