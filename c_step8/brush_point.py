"""塗った円
"""


class BrushPoint():
    """塗った円
    """

    def __init__(self):
        self.__distance = 0
        self.__range = 0

    @property
    def distance(self):
        """レールからの距離"""
        return self.__distance

    @distance.setter
    def distance(self, val):
        self.__distance = val

    @property
    def range(self):
        """塗った円の半径"""
        return self.__range

    @range.setter
    def range(self, val):
        self.__range = val
