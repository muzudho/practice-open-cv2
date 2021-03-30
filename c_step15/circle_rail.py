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
        self.__fitted_red_p = (0, 0)
        self.__fitted_green_p = (0, 0)
        self.__fitted_blue_p = (0, 0)
        self.__theta = 0

    @property
    def range(self):
        """半径"""
        return self.__range

    @property
    def diameter(self):
        """直径"""
        return 2*self.__range

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
        """角度"""
        return self.__theta

    @theta.setter
    def theta(self, theta):
        """円周上の点の位置を設定"""

        self.__theta = theta
        rng = self.range
        # 円周上の赤い点の位置
        self.__red_p = (int(rng * math.sin(math.radians(theta)) + self.center[0]),
                        int(-rng * math.cos(math.radians(theta)) + self.center[1]))  # yは上下反転

        # 円周上の緑の点の位置
        self.__green_p = (int(rng * math.sin(math.radians(theta-120)) + self.center[0]),
                          int(-rng * math.cos(math.radians(theta-120)) +
                              self.center[1]))

        # 円周上の青の点の位置
        self.__blue_p = (int(rng * math.sin(math.radians(theta+120)) + self.center[0]),
                         int(-rng * math.cos(math.radians(theta+120)) +
                             self.center[1]))

    def calc_fitted_p(self, n3bars_multiple):
        """円周上の点の位置を設定"""

        theta = self.__theta

        # 円周上の赤い点の位置
        rng2 = self.range * n3bars_multiple[0]
        self.__fitted_red_p = (int(rng2 * math.sin(math.radians(theta)) + self.center[0]),
                               int(-rng2 * math.cos(math.radians(theta)) + self.center[1]))

        # 円周上の緑の点の位置
        rng2 *= self.range * n3bars_multiple[1]
        self.__fitted_green_p = (int(rng2 * math.sin(math.radians(theta-120)) + self.center[0]),
                                 int(-rng2 * math.cos(math.radians(theta-120)) +
                                     self.center[1]))

        # 円周上の青の点の位置
        rng2 *= self.range * n3bars_multiple[2]
        self.__fitted_blue_p = (int(rng2 * math.sin(math.radians(theta+120)) + self.center[0]),
                                int(-rng2 * math.cos(math.radians(theta+120)) +
                                    self.center[1]))

    @property
    def red_p(self):
        """円周上の赤の点の位置"""
        return self.__red_p

    @property
    def green_p(self):
        """円周上の緑の点の位置"""
        return self.__green_p

    @property
    def blue_p(self):
        """円周上の青の点の位置"""
        return self.__blue_p

    @property
    def fitted_red_p(self):
        """円周上の赤の点の位置"""
        return self.__fitted_red_p

    @property
    def fitted_green_p(self):
        """円周上の緑の点の位置"""
        return self.__fitted_green_p

    @property
    def fitted_blue_p(self):
        """円周上の青の点の位置"""
        return self.__fitted_blue_p

    @property
    def upper_bound_y(self):
        """上限"""
        return min(self.red_p[1], self.green_p[1], self.blue_p[1])

    @property
    def lower_bound_y(self):
        """下限"""
        return max(self.red_p[1], self.green_p[1], self.blue_p[1])

    @property
    def inner_height(self):
        """上限と下限の差分の長さ"""
        return self.lower_bound_y - self.upper_bound_y  # yは逆さ

    @property
    def zoom(self):
        """直径に対するinner_heightの割合。0.0～1.0"""
        return self.inner_height / self.diameter

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
