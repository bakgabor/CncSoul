from app.event.event import Event
from app.service.abstract_service import AbstractService
from services.serial.cnc_interface import CncInterface
from services.serial.models.cnc_status import CncStatus
from services.serial.serial_connection import SerialConnection
from time import sleep


class CncSelector (AbstractService, Event):

    def __init__(self, servie_container):
        super().__init__(servie_container)
        self._serial: SerialConnection = self._get_service('serial_connection')

        self._serial.connect_event('read', self._check_connect)
        self._status: CncStatus = self._get_service('cnc_status')

        self._grbl_controller: CncInterface = self._get_service('grbl_control')
        self._printer_controller: CncInterface = self._get_service('printer_control')

        self._all_runners = [
            self._grbl_controller,
            self._printer_controller
        ]

        self._events = {
            'connect': [],
            'disconnect': []
        }

        self._cnc_runner = None

    def set_port(self, port):
        self._serial.set_port(port)

    def set_bit_rade(self, bit_rade):
        self._serial.set_bit_rade(bit_rade)

    def connect_runner_event(self, event, function):
        for runner in self._all_runners:
            runner.connect_event(event, function)

    def connect(self):
        self._serial.connect()

    def disconnect(self):
        self._cnc_runner.set_active(False)
        sleep(0.4)
        self._serial.disconnect()
        self._run_event('disconnect')
        self._cnc_runner = None

    def is_connected(self):
        return self._serial.is_connected()

    def get_ports(self):
        return self._serial.get_ports()

    def _check_connect(self, data):
        if data.find('Grbl') != -1:
            self._connect_to(self._grbl_controller)
            return
        if data.find('wait') != -1:
            if self._cnc_runner is None:
                self._connect_to(self._printer_controller)

    def _connect_to(self, runner):
        self._cnc_runner = runner
        self._cnc_runner.set_active(True)
        self._run_event('connect', arguments=(self._cnc_runner,))
