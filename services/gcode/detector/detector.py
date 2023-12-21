from services.gcode.utils.line_operations import point_and_line_collision, distance


class Detector:

    def __init__(self, line=None):
        self._line = line
        self._size = None
        if line is not None:
            self._calculate_size()

    def get_line(self):
        return self._line

    def set_line(self, line):
        self._line = line
        self._calculate_size()

    def detect(self, point, buffer_num=0.5):
        return point_and_line_collision(
            point, self._line.get_first_point(),
            self._line.get_second_point(),
            buffer_num
        )

    def get_size(self):
        return self._size

    def set_size(self, _size):
        self._size = _size

    def _calculate_size(self):
        self._size = distance(
            self._line.get_first_point(),
            self._line.get_second_point()
        )

    def __str__(self):
        return str(self._line)
