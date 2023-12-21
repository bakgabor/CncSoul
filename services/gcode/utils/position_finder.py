from services.gcode.utils.position import Position


class PositionFinder:

    def __init__(self, codeList):
        self.codeList = codeList
        self.pos = None

    def find(self, index):
        self.pos = Position(None, None, None)
        counter = 0
        if self.codeList.count() - 1 < index:
            index = self.codeList.count() - 1

        while not self.pos.checkAll() and (index - counter) != 0:
            code = self.codeList.getCode(index - counter)
            if not self.pos.checkX():
                self.pos.setX(code.get('X'))
            if not self.pos.checkY():
                self.pos.setY(code.get('Y'))
            if not self.pos.checkZ():
                self.pos.setZ(code.get('Z'))
            counter += 1

        return self.pos
