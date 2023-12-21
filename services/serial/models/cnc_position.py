
class CncPosition:

    def __init__(self, pos=None):
        self._index = {
            'X': 0,
            'Y': 1,
            'Z': 2,
            'A': 3,
            'B': 4,
            'E': 5
        }
        self._pos = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        if pos:
            self.set_all(pos)

    def set_pos(self, index, pos):
        index = self._index[index]
        self._pos[index] = float(pos)

    def get_pos(self, index):
        index = self._index[index]
        return self._pos[index]

    def get_all(self, dimension=None):
        if dimension:
            return self._pos[:dimension]
        return self._pos

    def set_all(self, array):
        for index, item in enumerate(array):
            self._pos[index] = float(item)

    def get_x(self):
        return self._pos[0]

    def set_x(self, value):
        self._pos[0] = value
        return self

    def get_y(self):
        return self._pos[1]

    def set_y(self, value):
        self._pos[1] = value
        return self

    def get_z(self):
        return self._pos[2]

    def set_z(self, value):
        self._pos[2] = value
        return self

    def get_a(self):
        return self._pos[3]

    def set_a(self, value):
        self._pos[3] = value
        return self

    def get_b(self):
        return self._pos[4]

    def set_b(self, value):
        self._pos[4] = value
        return self

    def __str__(self):
        string_var = '['
        for item in self._pos:
            string_var += str(item) + ', '
        string_var = string_var[:-2] + ']'
        return string_var
