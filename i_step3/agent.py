"""エージェント
"""


class Agent():
    """エージェント
    """

    def __init__(self):
        self.__location = (0, 0)

    @property
    def location(self):
        """居場所"""
        return self.__location

    @location.setter
    def location(self, val):
        self.__location = val
