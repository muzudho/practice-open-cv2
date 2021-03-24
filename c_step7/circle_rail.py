"""円レール
"""


class CircleRail():
    """円レール
    """

    def __init__(self):
        self.__range = 0
        self.__top = 0
        self.__center = (0, 0)

    @property
    def range(self):
        """半径"""
        return self.__range

    @range.setter
    def range(self, val):
        self.__range = val

    @property
    def top(self):
        """上端"""
        return self.__top

    @top.setter
    def top(self, val):
        self.__top = val

    @property
    def center(self):
        """中心座標"""
        return self.__center

    @center.setter
    def center(self, val):
        self.__center = val
