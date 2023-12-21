##
# Author: Bak Gabor
##
from services.gcode.gcode_model import GCode


class LinearInterpolation:

    def __init__(self, x=0, y=0, z=0, speed=1000):
        self._code = GCode()
        self._code.set('G', 1).set('X', x).set('Y', y).set('Z', z).set('F', speed)

    def build(self):
        return self._code
