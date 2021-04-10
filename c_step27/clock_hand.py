"""時計の針"""

import math
import cv2
from colors import PALE_GRAY
from conf import BAR_TICKS
from cv2_helper import color_for_cv2, point_for_cv2


class ClockHand():
    """時計の針"""

    def __init__(self):
        self.__center = (0, 0)
        self.__theta = 0
        self.__unit_arc = 0
        self.__tickness = 0
        self.__radius1 = 0
        self.__radius2 = 0
        self.__radius3 = 0

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
    def radius1(self):
        """半径の長さ"""
        return self.__radius1

    @radius1.setter
    def radius1(self, val):
        self.__radius1 = val

    @property
    def radius2(self):
        """半径の長さ"""
        return self.__radius2

    @radius2.setter
    def radius2(self, val):
        self.__radius2 = val

    @property
    def radius3(self):
        """半径の長さ"""
        return self.__radius3

    @radius3.setter
    def radius3(self, val):
        self.__radius3 = val

    def draw_clock_hand(self, canvas):
        """時計の針を描きます"""
        inner_p = (
            self.radius1 * math.cos(self.theta) +
            self.center[0],
            -self.radius1 * math.sin(self.theta)+self.center[1])
        outer_p = (
            self.radius2 *
            math.cos(self.theta)+self.center[0],
            -self.radius2 * math.sin(self.theta)
            + self.center[1])
        cv2.line(canvas,
                 point_for_cv2(inner_p),
                 point_for_cv2(outer_p),
                 color_for_cv2(PALE_GRAY, BAR_TICKS),
                 thickness=2)
        # 時計の針の先
        # 楕円、描画する画像を指定、座標(x,y),xyの半径、角度,色、線の太さ(-1は塗りつぶし)
        start_angle = int(math.degrees(self.theta) - self.unit_arc/2)
        end_angle = int(math.degrees(self.theta) + self.unit_arc/2)
        if start_angle == end_angle:
            end_angle += 1  # 差が 0 だと変なとこ描画するんで
        cv2.ellipse(canvas,
                    point_for_cv2(self.center),
                    point_for_cv2((self.radius2, self.radius2)),
                    0,
                    360-start_angle,
                    360-end_angle,
                    color_for_cv2(PALE_GRAY, BAR_TICKS),
                    thickness=int(self.tickness))
        cv2.ellipse(canvas,
                    point_for_cv2(self.center),
                    point_for_cv2((self.radius3, self.radius3)),
                    0,
                    360-start_angle,
                    360-end_angle,
                    color_for_cv2(PALE_GRAY, BAR_TICKS),
                    thickness=int(self.tickness))
