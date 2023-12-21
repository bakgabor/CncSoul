##
# Author: Bak Gabor
##
from services.gcode.gcode_model import GCode
from services.gcode.utils.position import Position


class GCodeList:

    def __init__(self, codes=None):
        if codes is None:
            codes = []
        self._gCodes = []
        self._lastPosition = Position()

        self._buildGenerators(codes)

        self._selected_line = 0

    def addCodeSting(self, code_string):
        code = GCode(code_string)
        self._lastPosition.setX(code.get('X')).setY(code.get('Y')).setZ(code.get('Z'))
        self._gCodes.append(code)

    def set_selected_line(self, line):
        self._selected_line = line - 1

    def get_selected_line(self):
        return self._selected_line

    def get_next_line(self):
        if len(self._gCodes) - 1 >= self._selected_line + 1:
            self._selected_line += 1
            return self._gCodes[self._selected_line]
        return None

    def getCode(self, index):
        return self._gCodes[index]

    def addCode(self, code):
        self._gCodes.append(code)
        self._lastPosition.setX(code.get('X')).setY(code.get('Y')).setZ(code.get('Z'))

    def saveToFile(self, path):
        file = ''
        for code in self._gCodes:
            file += str(code)

        with open(path, 'w') as f:
            f.write(file)
        print('save:' + path)
        return self

    def count(self):
        return len(self._gCodes)

    def getBunch(self, start, end):
        return self._gCodes[start:end]

    def getLastPosition(self):
        return self._lastPosition

    def clear(self):
        self._gCodes = []

    def _buildGenerators(self, generators):
        for generator in generators:
            self._buildGenerator(generator)

    def _buildGenerator(self, generator):
        generatedCode = generator.build()
        if isinstance(generatedCode, list):
            for code in generatedCode:
                self.addCode(code)
            return
        self.addCode(generatedCode)

    def build(self):
        return self._gCodes

    def __len__(self):
        return len(self._gCodes)
