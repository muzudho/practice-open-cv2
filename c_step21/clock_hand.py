"""時計の針"""


class ClockHand():
    """時計の針"""

    def __init__(self):
        self.__tickness = 0
        self.__rng1 = 0
        self.__rng2 = 0
        self.__rng3 = 0

    @property
    def tickness(self):
        """線の太さ"""
        return self.__tickness

    @tickness.setter
    def tickness(self, val):
        self.__tickness = val

    @property
    def rng1(self):
        """半径の長さ"""
        return self.__rng1

    @rng1.setter
    def rng1(self, val):
        self.__rng1 = val

    @property
    def rng2(self):
        """半径の長さ"""
        return self.__rng2

    @rng2.setter
    def rng2(self, val):
        self.__rng2 = val

    @property
    def rng3(self):
        """半径の長さ"""
        return self.__rng3

    @rng3.setter
    def rng3(self, val):
        self.__rng3 = val
