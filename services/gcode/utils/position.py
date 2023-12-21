##
# Author: Bak Gabor
##

class Position:

    def __init__(self, posX=None, posY=None, posZ=None):
        self._posX = posX
        self._posY = posY
        self._posZ = posZ

    def __str__(self):
        return 'X:' + str(self._posX) +\
               ' Y:' + str(self._posY) +\
               ' Z:' + str(self._posZ)

    def checkAll(self):
        return self._posX is not None and self._posY is not None and self._posZ is not None

    def checkX(self):
        return self._posX is not None

    def checkY(self):
        return self._posY is not None

    def checkZ(self):
        return self._posZ is not None

    def getX(self):
        return str(self._posX)

    def getY(self):
        return str(self._posY)

    def getZ(self):
        return str(self._posZ)

    def setX(self, x):
        if x is not None:
            self._posX = x
        return self

    def setY(self, y):
        if y is not None:
            self._posY = y
        return self

    def setZ(self, z):
        if z is not None:
            self._posZ = z
        return self
