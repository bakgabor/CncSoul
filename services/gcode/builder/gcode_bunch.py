##
# Author: Bak Gabor
##

class GCodeBunch:
    def __init__(self, bunch=None):
        if bunch is None:
            bunch = []
        self._bunch = bunch

    def build(self):
        return self._bunch
