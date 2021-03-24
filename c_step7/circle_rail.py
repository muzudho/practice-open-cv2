"""円レール
"""


class CircleRail():
    """円レール
    """

    def __init__(self):
        self.__range = 0

    @property
    def range(self):
        """半径"""
        return self.__range

    @range.setter
    def range(self, val):
        self.__range = val
