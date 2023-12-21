from services.serial.models.cnc_config import CncConfig
from services.serial.models.cnc_status import CncStatus


class GrblConfigDeserializer:

    def __init__(self, status: CncStatus):
        self._status: CncStatus = status
        self._config: CncConfig = status.get_config()
        self.codes = {
            'G0': 'driving_mode',
            'G1': 'driving_mode',
            'G2': 'driving_mode',
            'G3': 'driving_mode',
            'G38.2': 'driving_mode',
            'G38.3': 'driving_mode',
            'G38.4': 'driving_mode',
            'G38.5': 'driving_mode',
            'G80': 'driving_mode',
            'G54': 'coordinate_systems',
            'G55': 'coordinate_systems',
            'G56': 'coordinate_systems',
            'G57': 'coordinate_systems',
            'G58': 'coordinate_systems',
            'G59': 'coordinate_systems',
            'G17': 'plane',
            'G18': 'plane',
            'G19': 'plane',
            'G90': 'distances',
            'G91': 'distances',
            'G91.1': 'arc',
            'G93': 'submissions',
            'G94': 'submissions',
            'G20': 'units',
            'G21': 'units',
            'G40': 'cutter_radius_correction',
            'G43.1': 'tool_length_correction',
            'G49': 'tool_length_correction',
            'M0': 'program_mode',
            'M1': 'program_mode',
            'M2': 'program_mode',
            'M30': 'program_mode',
            'M3': 'spindle_condition',
            'M4': 'spindle_condition',
            'M5': 'spindle_condition',
            'M7': 'coolant_status',
            'M8': 'coolant_status',
            'M9': 'coolant_status',
        }

    def deserialize(self, data):
        state = data.split(":")
        if len(state) > 1:
            states = state[1][:-1]
            state_array = states.split(" ")
            for data in state_array:
                if data in self.codes:
                    self._config.add(self.codes[data], data)
                if data[0] == 'T':
                    self._config.add('active_tool_number', data[1:])
                if data[0] == 'S':
                    self._config.add('spindle_speed', data[1:])
                if data[0] == 'F':
                    self._config.add('feed', data[1:])
