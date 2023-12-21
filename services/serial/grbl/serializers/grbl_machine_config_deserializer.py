from services.serial.models.cnc_config import CncConfig
from services.serial.models.cnc_status import CncStatus


class GrblMachineConfigDeserializer:

    def __init__(self, status: CncStatus):
        self._status: CncStatus = status
        self._config: CncConfig = status.get_config()

    def deserialize(self, data):
        parameter_array = data.split("=")
        if len(parameter_array) > 1:
            self._config.add_machine_config(parameter_array[0], parameter_array[1])
