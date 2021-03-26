"""塗った円
"""

import math
import cv2


class BrushPoint():
    """塗った円
    """

    def __init__(self):
        self.__origin = (0, 0)
        self.__distance = 0
        self.__range = 0
        self.__location = (0, 0)

    @property
    def origin(self):
        """起点の座標"""
        return self.__origin

    @origin.setter
    def origin(self, val):
        self.__origin = val

    @property
    def distance(self):
        """レールからの距離"""
        return self.__distance

    @distance.setter
    def distance(self, val):
        self.__distance = val

    @property
    def range(self):
        """塗った円の半径"""
        return self.__range

    @range.setter
    def range(self, val):
        self.__range = val

    @property
    def location(self):
        """座標"""
        return self.__location

    @location.setter
    def location(self, val):
        self.__location = val

    def set_theta(self, val):
        """角度を設定"""
        self.__location = (
            int(self.distance * math.sin(math.radians(val)) + self.origin[0]),
            int(-self.distance * math.cos(math.radians(val)) + self.origin[1]))  # yは上下反転

    def draw_me(self, canvas, color):
        """描きます"""
        cv2.circle(canvas, self.location,
                   self.range, color, thickness=-1)
