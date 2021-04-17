"""キャンバスを盤として捉えます"""


class Board():
    """キャンバスを盤として捉えます"""

    def __init__(self):
        self.__rows = []
        self.__start_location = (0, 0)
        self.__width = 0
        self.__height = 0

    @property
    def rows(self):
        """テーブル"""
        return self.__rows

    @property
    def start_location(self):
        """スタート地点"""
        return self.__start_location

    @start_location.setter
    def start_location(self, val):
        self.__start_location = val

    @property
    def width(self):
        """列数"""
        return self.__width

    @width.setter
    def width(self, val):
        self.__width = val

    @property
    def height(self):
        """行数"""
        return self.__height

    @height.setter
    def height(self, val):
        self.__height = val
