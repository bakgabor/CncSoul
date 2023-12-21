class DetectorList:

    def __init__(self, detector_list=None):
        if detector_list is None:
            detector_list = []
        self._detector_list = detector_list
        self._size = 0

    def add_detector(self, detector):
        self._detector_list.append(detector)

    def detect(self, point, buffer_num=0.5):
        for detector in self._detector_list:
            if detector.detect(point, buffer_num):
                return True
        return False

    def set_size(self, size):
        self._size = size

    def get_size(self):
        return self._size
