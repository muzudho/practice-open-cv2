"""RGBバーが出てくる矩形
"""

import cv2
from colors import LIGHT_GRAY, RED, GREEN, BLUE, BLACK


class BarWindow():
    """RGBバーが出てくる矩形
    """

    def __init__(self):
        self.__left_top = (0, 0)
        self.__right_bottom = (0, 0)
        self.__one_width = 0
        self.__interval = 0
        self.__red_bar_p1 = (0, 0)
        self.__red_bar_p2 = (0, 0)
        self.__green_bar_p1 = (0, 0)
        self.__green_bar_p2 = (0, 0)
        self.__blue_bar_p1 = (0, 0)
        self.__blue_bar_p2 = (0, 0)

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
    def height(self):
        return self.__right_bottom[1] - self.__left_top[1]

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

    @property
    def red_bar_p1(self):
        """赤バーの左上点"""
        return self.__red_bar_p1

    @red_bar_p1.setter
    def red_bar_p1(self, val):
        self.__red_bar_p1 = val

    @property
    def red_bar_p2(self):
        """赤バーの右下点"""
        return self.__red_bar_p2

    @red_bar_p2.setter
    def red_bar_p2(self, val):
        self.__red_bar_p2 = val

    @property
    def green_bar_p1(self):
        """緑バーの左上点"""
        return self.__green_bar_p1

    @green_bar_p1.setter
    def green_bar_p1(self, val):
        self.__green_bar_p1 = val

    @property
    def green_bar_p2(self):
        """緑バーの右下点"""
        return self.__green_bar_p2

    @green_bar_p2.setter
    def green_bar_p2(self, val):
        self.__green_bar_p2 = val

    @property
    def blue_bar_p1(self):
        """青バーの左上点"""
        return self.__blue_bar_p1

    @blue_bar_p1.setter
    def blue_bar_p1(self, val):
        self.__blue_bar_p1 = val

    @property
    def blue_bar_p2(self):
        """青バーの右下点"""
        return self.__blue_bar_p2

    @blue_bar_p2.setter
    def blue_bar_p2(self, val):
        self.__blue_bar_p2 = val

    def draw_bars(self, canvas):
        """バーを描きます"""
        # バーR
        cv2.rectangle(canvas, self.red_bar_p1,
                      self.red_bar_p2, RED, thickness=-1)

        # バーG
        cv2.rectangle(canvas, self.green_bar_p1,
                      self.green_bar_p2, GREEN, thickness=-1)

        # バーB
        cv2.rectangle(canvas, self.blue_bar_p1,
                      self.blue_bar_p2, BLUE, thickness=-1)

    def get_upper_bound_y(self):
        """上限の座標"""
        return min(self.red_bar_p1[1], self.green_bar_p1[1], self.blue_bar_p1[1])

    def draw_horizontal_line(self, canvas, y_num):
        """水平線を描きます"""
        cv2.line(canvas, (self.red_bar_p1[0], y_num),
                 (self.blue_bar_p2[0], y_num), BLACK, thickness=2)

    @property
    def red_height(self):
        """赤バーの縦幅"""
        return self.red_bar_p2[1] - self.red_bar_p1[1]

    @property
    def green_height(self):
        """緑バーの縦幅"""
        return self.green_bar_p2[1] - self.green_bar_p1[1]

    @property
    def blue_height(self):
        """青バーの縦幅"""
        return self.blue_bar_p2[1] - self.blue_bar_p1[1]
