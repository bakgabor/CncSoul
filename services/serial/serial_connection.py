import threading

import serial.tools.list_ports
import serial
from sys import platform

from app.service.abstract_service import AbstractService
from app.event.event import Event


class SerialConnection (AbstractService, Event):

    def __init__(self, servie_container):
        super().__init__(servie_container)

        self._serial_open = False

        self._serial_name = None
        self._bit_rade = 115200
        self._serial = None

        self._events = {
            'send': [],
            'read': []
        }

    def send_bytes(self, data):
        self._serial.write(data)
        self._run_event('send', arguments=(data,))

    def send(self, data):
        self._serial.write(bytes(data, 'UTF-8'))
        self._run_event('send', arguments=(data,))

    def send_line(self, data):
        if self._serial_open:
            self._serial.write(bytes(data + '\n', 'UTF-8'))
            self._run_event('send', arguments=(data + '\n',))

    def get_ports(self):
        ports = []
        for port in serial.tools.list_ports.comports():
            ports.append(port.name)
        return ports

    def set_port(self, name):
        if name is None:
            return
        if platform == "linux" or platform == "linux2":
            self._serial_name = '/dev/' + name
        elif platform == "darwin":
            self._serial_name = '/dev/' + name
        elif platform == "win32":
            self._serial_name = name
        return self

    def set_bit_rade(self, bit_rade):
        self._bit_rade = bit_rade
        return self

    def is_connected(self):
        return self._serial_open

    def disconnect(self):
        self._serial_open = False
        self._serial.cancel_read()

    def connect(self):
        if self._serial_name:
            t = threading.Thread(target=self._connect_thread)
            t.start()

    def _connect_thread(self):
        self._serial_open = True
        self._serial = serial.Serial(self._serial_name, self._bit_rade)
        while self._serial_open:
            cc = str(self._serial.readline())
            if cc[2:][:-5]:
                self._run_event('read', arguments=(cc[2:][:-5],))
                # for event in self._read_events:
                #     # t = threading.Thread(target=event, args=(cc[2:][:-5],))
                #     # t.start()
                #     event(cc[2:][:-5])
        self._serial.close()
