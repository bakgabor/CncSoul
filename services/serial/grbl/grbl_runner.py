from app.event.event import Event
from services.gcode.detector.gcode_collision_detector import GcodeCollisionDetector
from services.gcode.gcode_list import GCodeList
from services.serial.models.cnc_position import CncPosition
from services.serial.models.cnc_status import CncStatus


class GrblRunner (Event):

    def __init__(self, grbl_control, cnc_status):
        super().__init__()

        self._events = {
            'next_command': [],
            'synchronization_error': [],
            'run_end': []
        }

        self._grbl_control = grbl_control
        self._grbl_control.connect_event('before_idle', self._run_next_code)
        self._grbl_control.connect_event('before_idle', self._check_end)
        self._grbl_control.connect_event('info', self._update_position)

        self._gcode: GCodeList or None = None
        self._status: CncStatus = cnc_status
        self._collision_detector = GcodeCollisionDetector()

        self._synchronization_error = False
        self._state = 's'

    def set_gcode(self, gcode):
        self._gcode: GCodeList = gcode
        return self

    def set_selected_line(self, line):
        self._gcode.set_selected_line(line)
        return self

    def run_code(self):
        if self._gcode:
            self._state = 'r'
            position = self._status.get_position()
            self._collision_detector.clear()
            self._collision_detector.set_last_position(position.get_all(3))
            for i in range(5):
                self._run_next_code()
            self._run_event('next_command', arguments=(self._collision_detector.get_gcode(0),))
        print('Run')

    def pause(self):
        status = self._status.get_status()
        info_array = status.split(":")
        if info_array[0] != 'Hold':
            self._grbl_control.send_command("!")
            return
        self._grbl_control.send_command('~')

    def stop(self):
        self._grbl_control.send_bytes([0x18, 0x0a])
        self._state = 's'

    def _run_next_code(self):
        if self._state == 'r':
            next_line = self._gcode.get_next_line()
            print(next_line)
            if next_line:
                self._collision_detector.add_gcode(next_line)
                self._grbl_control.send_command(str(next_line))

    def _check_end(self):
        if self._gcode:
            if self._state == 'r' and self._gcode.count() == self._gcode.get_selected_line() + 1:
                self._state = 's'
                self._run_event('run_end')
                print('End')

    def _update_position(self):
        local_position: CncPosition = self._status.get_local_position()
        index = self._collision_detector.detect(local_position.get_all(3))
        if index > 0:
            self._run_event('next_command', arguments=(self._collision_detector.get_gcode(1),))
            self._collision_detector.remove_first_elements()
            self._run_next_code()
            self._collision_detector.calc_max_min_distances()
        if self._state == 'r' and index == -1 and not self._synchronization_error:
            self._run_event('synchronization_error',)
            self._synchronization_error = True
        if index == 0:
            self._synchronization_error = False
