"""円レール
"""

import math

import cv2
from colors import RED, GREEN, BLUE, BLACK


class CircleRail():
    """円レール
    """

    def __init__(self):
        self.__range = 0
        self.__top = 0
        self.__center = (0, 0)
        self.__point_range = 0
        self.__red_p = (0, 0)
        self.__green_p = (0, 0)
        self.__blue_p = (0, 0)
        self.__theta = 0

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

    @property
    def theta(self):
        return self.__theta

    @theta.setter
    def theta(self, theta):
        """円周上の赤の点の角度を設定"""

        self.__theta = theta
        # 円周上の赤い点の位置
        self.red_p = (int(self.range * math.sin(math.radians(theta)) + self.center[0]),
                      int(-self.range * math.cos(math.radians(theta)) + self.center[1]))  # yは上下反転

        # 円周上の緑の点の位置
        self.green_p = (int(self.range * math.sin(math.radians(theta-120)) + self.center[0]),
                        int(-self.range * math.cos(math.radians(theta-120)) + self.center[1]))  # yは上下反転

        # 円周上の青の点の位置
        self.blue_p = (int(self.range * math.sin(math.radians(theta+120)) + self.center[0]),
                       int(-self.range * math.cos(math.radians(theta+120)) + self.center[1]))  # yは上下反転

    @property
    def red_p(self):
        """円周上の赤の点の位置"""
        return self.__red_p

    @red_p.setter
    def red_p(self, val):
        self.__red_p = val

    @property
    def green_p(self):
        """円周上の緑の点の位置"""
        return self.__green_p

    @green_p.setter
    def green_p(self, val):
        self.__green_p = val

    @property
    def blue_p(self):
        """円周上の青の点の位置"""
        return self.__blue_p

    @blue_p.setter
    def blue_p(self, val):
        self.__blue_p = val

    def upper_bound_y(self):
        return min(self.red_p[1], self.green_p[1], self.blue_p[1])

    def lower_bound_y(self):
        return max(self.red_p[1], self.green_p[1], self.blue_p[1])

    def draw_red_p(self, canvas):
        """円周上の点Rを描きます"""
        cv2.circle(canvas, self.red_p,
                   self.point_range, RED, thickness=-1)

    def draw_green_p(self, canvas):
        """円周上の点Gを描きます"""
        cv2.circle(canvas, self.green_p,
                   self.point_range, GREEN, thickness=-1)

    def draw_blue_p(self, canvas):
        """円周上の点Bを描きます"""
        cv2.circle(canvas, self.blue_p,
                   self.point_range, BLUE, thickness=-1)

    def draw_me(self, canvas):
        """描きます"""
        # 円レール。描画する画像を指定、座標（x,y),半径、色、線の太さ（-1は塗りつぶし）
        cv2.circle(canvas, self.center,
                   self.range, BLACK, thickness=2)
