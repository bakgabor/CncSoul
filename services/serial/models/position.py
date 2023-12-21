class Position:

    def __init__(self):
        self._pos_x = 0
        self._pos_y = 0
        self._pos_z = 0
        self._pos_a = 0
        self._pos_b = 0

    def serialize(self, data):
        pos_array = data.split(",")
        length = len(pos_array)
        if length > 0:
            self._pos_x = float(pos_array[0])
        if length > 1:
            self._pos_y = float(pos_array[1])
        if length > 2:
            self._pos_z = float(pos_array[2])
        if length > 3:
            self._pos_a = float(pos_array[3])
        if length > 4:
            self._pos_b = float(pos_array[4])

    def get_pos_x(self):
        return self._pos_x

    def set_pos_x(self, pos_x):
        self._pos_x = pos_x

    def get_pos_y(self):
        return self._pos_y

    def set_pos_y(self, pos_y):
        self._pos_y = pos_y

    def get_pos_z(self):
        return self._pos_z

    def set_pos_z(self, pos_z):
        self._pos_z = pos_z

    def get_pos_a(self):
        return self._pos_a

    def set_pos_a(self, pos_a):
        self._pos_a = pos_a

    def get_pos_b(self):
        return self._pos_b

    def set_pos_b(self, pos_b):
        self._pos_b = pos_b
