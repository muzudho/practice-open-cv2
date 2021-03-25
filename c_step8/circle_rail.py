"""円レール
"""

import math


class CircleRail():
    """円レール
    """

    def __init__(self):
        self.__range = 0
        self.__top = 0
        self.__center = (0, 0)
        self.__point_range = 0

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

    @property
    def point_range(self):
        """円周上の点の半径"""
        return self.__point_range

    @point_range.setter
    def point_range(self, val):
        self.__point_range = val

    def calc_red_p(self, theta):
        """円周上の赤い点の位置"""
        return (int(self.range * math.sin(math.radians(theta)) + self.center[0]),
                int(-self.range * math.cos(math.radians(theta)) + self.center[1]))  # yは上下反転

    def calc_green_p(self, theta):
        """円周上の緑の点の位置"""
        return (int(self.range * math.sin(math.radians(theta-120)) + self.center[0]),
                int(-self.range * math.cos(math.radians(theta-120)) + self.center[1]))  # yは上下反転

    def calc_blue_p(self, theta):
        """円周上の青の点の位置"""
        return (int(self.range * math.sin(math.radians(theta+120)) + self.center[0]),
                int(-self.range * math.cos(math.radians(theta+120)) + self.center[1]))  # yは上下反転
