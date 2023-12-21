##
# Author: Bak Gabor
##

import re


class GCode:

    def __init__(self, code=None):
        self._operation = {}

        self._selectedAttribute = ''
        self._isComment = False
        self._comments = None

        if code:
            self.setCode(code)

    def __str__(self):
        text = ''
        for key in self._operation:
            text += self._getOperationText(key)
        text = text[:-1]
        if self._comments:
            for comment in self._comments:
                text += '(' + comment + ')'
        return text + '\n'

    def get(self, operation):
        if operation in self._operation:
            return self._operation[operation]
        return None

    def set(self, operation, value):
        if operation and value:
            self._operation[operation] = value
        return self

    def setCode(self, code):
        self._comments = [x.group() for x in re.finditer(r'((?<=\()(.*?)(?=\)))', code)]
        codes = [x.group() for x in re.finditer(r'[a-zA-Z](-?\d+(\.\d+)?)', code)]
        for operation in codes:
            self._addToOperation(operation)

    def _addToOperation(self, operation):
        key = operation[0]
        if key in self._operation:
            if not isinstance(self._operation[key], list):
                old = self._operation[key]
                self._operation[key] = [old, operation[1:]]
                return
            self._operation[key].append(operation[1:])
            return
        self._operation[key] = operation[1:]

    def _getOperationText(self, key):
        if isinstance(self._operation[key], list):
            text = ''
            for operation in self._operation[key]:
                text += str(key) + str(operation) + ' '
            return text
        return str(key) + str(self._operation[key]) + ' '
