"""円レール
"""

import math

import cv2
from colors import PALE_GRAY, PALE_RED, PALE_GREEN, PALE_BLUE
from rectangle import Rectangle
from triangle import Triangle
from conf import GRID_UNIT
from cv2_helper import color_for_cv2, point_for_cv2


class CircleRail():
    """円レール
    """

    def __init__(self):
        self.__drawing_top = 0
        self.__drawing_bottom = 0
        self.__border_rect = Rectangle()

        self.__radius = 0
        self.__center = (0, 0)
        self.__theta = 0
        self.__triangle = Triangle()
        self.__triangle.edge_color = PALE_GRAY
        self.__triangle.node_radius = GRID_UNIT / 2
        self.__triangle.nodes_color = (
            PALE_RED, PALE_BLUE, PALE_GREEN)  # 緑と青が逆なのが工夫
        self.__triangle.center_color = PALE_GRAY

    @property
    def radius(self):
        """半径"""
        return self.__radius

    @property
    def diameter(self):
        """直径"""
        return 2*self.__radius

    @property
    def border_rect(self):
        """境界線の矩形"""
        return self.__border_rect

    @border_rect.setter
    def border_rect(self, val):
        self.__border_rect = val

    @property
    def drawing_top(self):
        """上下の境界線の上端"""
        return self.__drawing_top

    @drawing_top.setter
    def drawing_top(self, val):
        self.__drawing_top = val

    @property
    def drawing_bottom(self):
        """上下の境界線の下端"""
        return self.__drawing_bottom

    @drawing_bottom.setter
    def drawing_bottom(self, val):
        self.__drawing_bottom = val

    @radius.setter
    def radius(self, val):
        self.__radius = val

    @property
    def center(self):
        """中心座標"""
        return self.__center

    @center.setter
    def center(self, val):
        self.__center = val

    @property
    def theta(self):
        """角度"""
        return self.__theta

    @theta.setter
    def theta(self, theta):
        """円周上の点の位置を設定"""

        self.__theta = theta
        radius = self.radius
        # 円周上の赤い点の位置

        red_p = (radius * math.cos(theta) + self.center[0],
                 -radius * math.sin(theta) + self.center[1])  # yは上下反転

        # 円周上の緑の点の位置
        green_p = (radius * math.cos(theta-math.radians(120)) + self.center[0],
                   -radius * math.sin(theta-math.radians(120)) +
                   self.center[1])

        # 円周上の青の点の位置
        blue_p = (radius * math.cos(theta+math.radians(120)) + self.center[0],
                  -radius * math.sin(theta+math.radians(120)) +
                  self.center[1])
        self.__triangle.nodes_p = (red_p, green_p, blue_p)

    @property
    def triangle(self):
        """円に内接する三角形"""
        return self.__triangle

    @property
    def upper_bound_y(self):
        """上限"""
        return min(
            self.__triangle.nodes_p[0][1],
            self.__triangle.nodes_p[0][1], self.__triangle.nodes_p[0][1])

    @property
    def lower_bound_y(self):
        """下限"""
        return max(
            self.__triangle.nodes_p[0][1],
            self.__triangle.nodes_p[0][1], self.__triangle.nodes_p[0][1])

    @property
    def inner_height(self):
        """上限と下限の差分の長さ"""
        return self.lower_bound_y - self.upper_bound_y  # yは逆さ

    @property
    def zoom(self):
        """直径に対するinner_heightの割合。0.0～1.0"""
        return self.inner_height / self.diameter

    def draw_circle(self, canvas):
        """描きます"""
        # 円レール。描画する画像を指定、座標（x,y),半径、色、線の太さ（-1は塗りつぶし）
        cv2.circle(canvas,
                   point_for_cv2(self.center),
                   int(self.radius),
                   color_for_cv2(PALE_GRAY),
                   thickness=2)

    def draw_triangle(self, canvas):
        """円に内接する線。正三角形"""
        self.__triangle.draw(canvas)
