"""外環状"""

import cv2
from conf import GRID_UNIT


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

    def draw_me(self, canvas):
        """描きます"""
        # 色相環
        color_count = len(self.color_list)
        # print(
        #    f"color_count={color_count} self.area_size=({self.area_size[0]}, {self.area_size[1]})")
        for i in range(0, color_count):
            theta = i * self.unit_arc
            color = self.color_list[i]
            # print(f"[{i}] theta={theta} color={color}")

            # 円弧
            # 楕円、描画する画像を指定、座標(x,y),xyの半径、角度,色、線の太さ(-1は塗りつぶし)
            start_angle = int(theta-self.unit_arc/2)
            end_angle = int(theta+self.unit_arc/2)
            if start_angle == end_angle:
                end_angle += 1  # 差が 0 だと変なとこ描画するんで
            cv2.ellipse(canvas,
                        self.origin,
                        self.area_size,
                        -90,
                        start_angle,
                        end_angle,
                        color,
                        thickness=int(1.25*GRID_UNIT))
