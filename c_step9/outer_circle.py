"""外環状"""

import cv2
from color_calc import calc_color, calc_step2
from conf import GRID_INTERVAL_H


class OuterCircle():
    """外環状"""

    def __init__(self):
        self.__origin = (0, 0)
        self.__area_size = (0, 0)
        self.__phase = 0
        self.__phases = 1  # 位相の段階数
        self.__circumference = 360  # 半径１の円の一周の長さ
        self.__unit_arc = self.__circumference/self.__phases  # 等分割した１つの弧
        self.__color_list = []

    @property
    def origin(self):
        """起点の座標"""
        return self.__origin

    @origin.setter
    def origin(self, val):
        self.__origin = val

    @property
    def area_size(self):
        """描画領域のサイズ"""
        return self.__area_size

    @area_size.setter
    def area_size(self, val):
        self.__area_size = val

    @property
    def phase(self):
        """位相"""
        return self.__phase

    @phase.setter
    def phase(self, val):
        self.__phase = val
        self.__unit_arc = self.__circumference/self.__phases  # 等分割した１つの弧

    @property
    def phases(self):
        """位相の段階数"""
        return self.__phases

    @phases.setter
    def phases(self, val):
        self.__phases = val

    @property
    def unit_arc(self):
        """等分割した１つの弧"""
        return self.__unit_arc

    @unit_arc.setter
    def unit_arc(self, val):
        self.__unit_arc = val

    @property
    def color_list(self):
        """色のリスト"""
        return self.__color_list

    @color_list.setter
    def color_list(self, val):
        self.__color_list = val

    def draw_me(self, canvas, bar_rates, ceil_height, base_line):
        """描きます"""
        # 色相環
        color_count = len(self.color_list)
        for i in range(0, color_count):
            theta = i * self.unit_arc
            print(f"i={i} color_count={color_count}")
            color = self.color_list[i]
            # print(f"[{i}] color={color}")

            # 円弧
            # 楕円、描画する画像を指定、座標(x,y),xyの半径、角度,色、線の太さ(-1は塗りつぶし)
            cv2.ellipse(canvas,
                        self.origin,
                        self.area_size,
                        -90,
                        theta,
                        theta+self.unit_arc,
                        color,
                        thickness=int(GRID_INTERVAL_H*3/2))
