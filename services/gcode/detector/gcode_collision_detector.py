from services.gcode.detector.detector import Detector
from services.gcode.detector.detector_list import DetectorList
from services.gcode.detector.primitives.line import Line
from services.gcode.gcode_model import GCode
from services.gcode.utils.line_operations import expand_arc, arc_radius


class GcodeCollisionDetector:

    def __init__(self):
        self._last_position = [0.0, 0.0, 0.0]
        self._detector_list = []
        self._gcode_list = []

        self._min_size = 9999999.9
        self._max_size = 0.0
        self._buffer_num = 0.5

    def set_last_position(self, position):
        self._last_position = position

    def clear(self):
        self._detector_list = []
        self._gcode_list = []

    def remove_first_elements(self, remove=1):
        self._detector_list = self._detector_list[remove:]
        self._gcode_list = self._gcode_list[remove:]

    def add_gcode(self, gcode: GCode):
        g = gcode.get('G')
        self._gcode_list.append(gcode)
        if g == '2' or g == '02' or g == '3' or g == '03':
            self._create_circle_detector(gcode)
            return
        self._create_line_detector(gcode)

    def add_line(self, line):
        self._detector_list.append(line)

    def count(self):
        return len(self._detector_list)

    def detect(self, point):
        for index, detector in enumerate(self._detector_list):
            if detector.detect(point, self._buffer_num):
                return index
        return -1

    def get_gcode(self, index):
        return self._gcode_list[index]

    def calc_max_min_distances(self):
        for detector in self._detector_list:
            if self._min_size > detector.get_size():
                self._min_size = detector.get_size()
            if self._max_size < detector.get_size():
                self._max_size = detector.get_size()
        self._calc_buffer_number()

    def _create_circle_detector(self, gcode: GCode):
        circle = expand_arc(
            str(gcode),
            self._last_position[0],
            self._last_position[1],
            float(gcode.get('X') or self._last_position[0]),
            float(gcode.get('Y') or self._last_position[1]),
            float(gcode.get('I') or '0'),
            float(gcode.get('J') or '0')
        )
        radius = arc_radius(
            self._last_position[0],
            self._last_position[1],
            float(gcode.get('I') or '0'),
            float(gcode.get('J') or '0')
        )
        self._calculate_z_in_circle(
            circle,
            self._last_position[2],
            float(gcode.get('Z') or '0'),
            radius
        )
        self._last_position = circle[-1]

    def _calculate_z_in_circle(self, array, first_z, second_z, radius):
        z_step = abs(first_z - second_z) / (len(array) - 1)
        for index, item in enumerate(array):
            if first_z < second_z:
                array[index].append(round(first_z + index * z_step, 6))
            else:
                array[index].append(round(first_z - index * z_step, 6))
        self._array_to_detector(array, radius)

    def _array_to_detector(self, array, radius=0.0):
        detector_list = DetectorList()
        detector_list.set_size(radius)
        for index, item in enumerate(array):
            if index + 1 <= len(array) - 1:
                line = Line(first_point=item, second_point=array[index + 1])
                detector = Detector(line)
                detector_list.add_detector(detector)
        self._detector_list.append(detector_list)

    def _create_line_detector(self, gcode: GCode):
        second_point = [
            float(gcode.get('X') or self._last_position[0]),
            float(gcode.get('Y') or self._last_position[1]),
            float(gcode.get('Z') or self._last_position[2])
        ]
        line = Line(first_point=self._last_position, second_point=second_point)
        detector = Detector(line)
        self._detector_list.append(detector)
        self._last_position = [
            float(gcode.get('X') or self._last_position[0]),
            float(gcode.get('Y') or self._last_position[1]),
            float(gcode.get('Z') or self._last_position[2])
        ]

    def _calc_buffer_number(self):
        if 0.5 > self._min_size / 10:
            self._buffer_num = self._min_size / 10
            return
        self._buffer_num = 0.5
