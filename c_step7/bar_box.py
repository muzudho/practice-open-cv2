"""RGBバーの箱
"""


class BarBox():
    """RGBバーの箱
    """

    def __init__(self):
        self.__top2 = 0
        self.__top3 = 0
        self.__height1 = 0
        self.__height2 = 0
        self.__height3 = 0
        self.__one_width = 0
        self.__left = 0
        self.__right = 0
        self.__red_left = 0
        self.__green_left = 0
        self.__blue_left = 0
        self.__rank1_p1 = (0, 0)
        self.__rank1_p2 = (0, 0)

    @property
    def top2(self):
        """２段目の箱の上辺"""
        return self.__top2

    @top2.setter
    def top2(self, val):
        self.__top2 = val

    @property
    def top3(self):
        """３段目の箱の上辺"""
        return self.__top3

    @top3.setter
    def top3(self, val):
        self.__top3 = val

    @property
    def height1(self):
        """１段目の箱の縦幅"""
        return self.__height1

    @height1.setter
    def height1(self, val):
        self.__height1 = val

    @property
    def height2(self):
        """２段目の箱の縦幅"""
        return self.__height2

    @height2.setter
    def height2(self, val):
        self.__height2 = val

    @property
    def height3(self):
        """３段目の箱の縦幅"""
        return self.__height3

    @height3.setter
    def height3(self, val):
        self.__height3 = val

    @property
    def one_width(self):
        """バー１本分の幅"""
        return self.__one_width

    @one_width.setter
    def one_width(self, val):
        self.__one_width = val

    @property
    def left(self):
        """箱の左座標"""
        return self.__left

    @left.setter
    def left(self, val):
        self.__left = val

    @property
    def right(self):
        """箱の右座標"""
        return self.__right

    @right.setter
    def right(self, val):
        self.__right = val

    @property
    def red_left(self):
        """赤いバーの左座標"""
        return self.__red_left

    @red_left.setter
    def red_left(self, val):
        self.__red_left = val

    @property
    def green_left(self):
        """緑のバーの左座標"""
        return self.__green_left

    @green_left.setter
    def green_left(self, val):
        self.__green_left = val

    @property
    def blue_left(self):
        """青のバーの左座標"""
        return self.__blue_left

    @blue_left.setter
    def blue_left(self, val):
        self.__blue_left = val

    @property
    def rank1_p1(self):
        """１段目の箱の左上点"""
        return self.__rank1_p1

    @rank1_p1.setter
    def rank1_p1(self, val):
        self.__rank1_p1 = val

    @property
    def rank1_p2(self):
        """１段目の箱の右下点"""
        return self.__rank1_p2

    @rank1_p2.setter
    def rank1_p2(self, val):
        self.__rank1_p2 = val
