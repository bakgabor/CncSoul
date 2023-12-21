##
# Author: Bak Gabor
##

import os

from services.gcode.gcode_model import GCode


class GCodeFileLoader:

    def __init__(self, file):
        self._gCodes = []
        self._file = file or ''

    def count(self):
        return len(self._gCodes)

    def build(self):
        if os.path.isfile(self._file):
            with open(self._file, "r") as f:
                for count, line in enumerate(f):
                    print('load:' + self._file + ' line:' + str(count), end='\r')
                    self._gCodes.append(GCode(line))
            print('load:' + self._file + ' line:' + str(self.count()))
            return self._gCodes
        return []
