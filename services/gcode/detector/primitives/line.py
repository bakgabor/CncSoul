
class Line:

    def __init__(self, first_point=None, second_point=None):
        if second_point is None:
            second_point = [0, 0, 0]
        if first_point is None:
            first_point = [0, 0, 0]
        self._first_point = first_point
        self._second_point = second_point

    def get_first_point(self):
        return self._first_point

    def get_second_point(self):
        return self._second_point

    def set_first_point(self, first_point):
        self._first_point = first_point
        return self

    def set_second_point(self, second_point):
        self._second_point = second_point

    def __str__(self):
        text = '['
        for first in self._first_point:
            text += str(first) + ', '
        text = text[:-2]
        text += '] ['
        for second in self._second_point:
            text += str(second) + ', '
        text = text[:-2]
        text += ']'
        return text
