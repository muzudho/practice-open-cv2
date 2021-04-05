"""時計の針"""

import math
import cv2
from colors import PALE_GRAY
from color_calc import color_to_byte


class ClockHand():
    """時計の針"""

    def __init__(self):
        self.__center = (0, 0)
        self.__theta = 0
        self.__unit_arc = 0
        self.__tickness = 0
        self.__rng1 = 0
        self.__rng2 = 0
        self.__rng3 = 0

    @property
    def center(self):
        """円の中心"""
        return self.__center

    @center.setter
    def center(self, val):
        self.__center = val

    @property
    def theta(self):
        """角度"""
        return self.__theta

    @theta.setter
    def theta(self, val):
        self.__theta = val

    @property
    def unit_arc(self):
        """単位となる弧の長さ"""
        return self.__unit_arc

    @unit_arc.setter
    def unit_arc(self, val):
        self.__unit_arc = val

    @property
    def tickness(self):
        """線の太さ"""
        return self.__tickness

    @tickness.setter
    def tickness(self, val):
        self.__tickness = val

    @property
    def rng1(self):
        """半径の長さ"""
        return self.__rng1

    @rng1.setter
    def rng1(self, val):
        self.__rng1 = val

    @property
    def rng2(self):
        """半径の長さ"""
        return self.__rng2

    @rng2.setter
    def rng2(self, val):
        self.__rng2 = val

    @property
    def rng3(self):
        """半径の長さ"""
        return self.__rng3

    @rng3.setter
    def rng3(self, val):
        self.__rng3 = val

    def draw_clock_hand(self, canvas):
        inner_p = (
            int(self.rng1 * math.cos(math.radians(self.theta)) +
                self.center[0]),
            int(-self.rng1 * math.sin(math.radians(self.theta))+self.center[1]))
        outer_p = (
            int(self.rng2 *
                math.cos(math.radians(self.theta))+self.center[0]),
            int(-self.rng2 * math.sin(math.radians(self.theta))
                + self.center[1]))
        cv2.line(canvas, inner_p, outer_p,
                 color_to_byte(PALE_GRAY),
                 thickness=2)
        # 時計の針の先
        # 楕円、描画する画像を指定、座標(x,y),xyの半径、角度,色、線の太さ(-1は塗りつぶし)
        start_angle = int(self.theta - self.unit_arc/2)
        end_angle = int(self.theta + self.unit_arc/2)
        if start_angle == end_angle:
            end_angle += 1  # 差が 0 だと変なとこ描画するんで
        cv2.ellipse(canvas,
                    self.center,
                    (self.rng2, self.rng2),
                    0,
                    360-start_angle,
                    360-end_angle,
                    color_to_byte(PALE_GRAY),
                    thickness=self.tickness)
        cv2.ellipse(canvas,
                    self.center,
                    (self.rng3, self.rng3),
                    0,
                    360-start_angle,
                    360-end_angle,
                    color_to_byte(PALE_GRAY),
                    thickness=self.tickness)
