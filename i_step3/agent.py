"""エージェント
"""


class Agent():
    """エージェント
    """

    def __init__(self):
        self.__location = [0, 0]
        self.__prev_location = [0, 0]

    @property
    def location(self):
        """居場所"""
        return self.__location

    @location.setter
    def location(self, val):
        self.__location = val

    @property
    def prev_location(self):
        """１つ前の居場所"""
        return self.__prev_location

    @prev_location.setter
    def prev_location(self, val):
        self.__prev_location = val
