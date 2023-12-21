from services.serial.models.cnc_position import CncPosition
from services.serial.models.cnc_status import CncStatus


class PositionDeserializer:

    def __init__(self, status: CncStatus):
        self._status: CncStatus = status
        self._position: CncPosition = status.get_position()
        self._local_position: CncPosition = status.get_local_position()
        self._null_position: CncPosition = status.get_null_position()

    def deserialize(self, data):
        data_array = data.split(" ")
        for position in data_array:
            position_array = position.split(":")
            self._position.set_pos(position_array[0], position_array[1])
        self._create_local_position()

    def _create_local_position(self):
        self._local_position.set_x(self._position.get_x() - self._null_position.get_x())
        self._local_position.set_y(self._position.get_y() - self._null_position.get_y())
        self._local_position.set_z(self._position.get_z() - self._null_position.get_z())
