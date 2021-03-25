"""RGBバーが出てくる矩形
"""

import cv2
from colors import LIGHT_GRAY


class BarWindow():
    """RGBバーが出てくる矩形
    """

    def __init__(self):
        self.__left_top = (0, 0)
        self.__right_bottom = (0, 0)
        self.__one_width = 0
        self.__interval = 0

    @property
    def left_top(self):
        """箱の左上点"""
        return self.__left_top

    @left_top.setter
    def left_top(self, val):
        self.__left_top = val

    @property
    def right_bottom(self):
        """箱の右下点"""
        return self.__right_bottom

    @right_bottom.setter
    def right_bottom(self, val):
        self.__right_bottom = val

    @property
    def one_width(self):
        """バー１本分の幅"""
        return self.__one_width

    @one_width.setter
    def one_width(self, val):
        self.__one_width = val

    @property
    def interval(self):
        """バーの間隔"""
        return self.__interval

    @interval.setter
    def interval(self, val):
        self.__interval = val

    def draw_outline(self, canvas):
        """輪郭を描きます"""
        cv2.rectangle(canvas, self.left_top,
                      self.right_bottom, LIGHT_GRAY, thickness=4)
