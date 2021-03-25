"""RGBバーの箱
"""

import cv2
from colors import LIGHT_GRAY, BLACK, RED, GREEN, BLUE


class BarBox():
    """RGBバーの箱
    """

    def __init__(self):
        self.__rates = [0, 0, 0]
        self.__top1 = 0
        self.__top2 = 0
        self.__top3 = 0
        self.__height = 0
        self.__height1 = 0
        self.__height2 = 0
        self.__height3 = 0
        self.__one_width = 0
        self.__left = 0
        self.__right = 0
        self.__bottom = 0
        self.__red_left = 0
        self.__green_left = 0
        self.__blue_left = 0
        self.__rank1_p1 = (0, 0)
        self.__rank1_p2 = (0, 0)
        self.__rank2_p1 = (0, 0)
        self.__rank2_p2 = (0, 0)
        self.__rank3_p1 = (0, 0)
        self.__rank3_p2 = (0, 0)
        self.__red_bar_p1 = (0, 0)
        self.__red_bar_p2 = (0, 0)
        self.__green_bar_p1 = (0, 0)
        self.__green_bar_p2 = (0, 0)
        self.__blue_bar_p1 = (0, 0)
        self.__blue_bar_p2 = (0, 0)
        self.__font_height = 0
        self.__font_scale = 0
        self.__line_type = 0
        self.__font = None
        self.__red_addition = 0
        self.__green_addition = 0
        self.__blue_addition = 0

    @property
    def rates(self):
        """バー率"""
        return self.__rates

    @rates.setter
    def rates(self, val):
        self.__rates = val

    @property
    def top1(self):
        """１段目の箱の上辺"""
        return self.__top1

    @top1.setter
    def top1(self, val):
        self.__top1 = val

    @property
    def top2(self):
        """２段目の箱の上辺"""
        return self.__top2

    @top2.setter
    def top2(self, val):
        self.__top2 = val

    @property
    def top3(self):
        """３段目の箱の上辺"""
        return self.__top3

    @top3.setter
    def top3(self, val):
        self.__top3 = val

    @property
    def height(self):
        """箱の縦幅"""
        return self.__height

    @height.setter
    def height(self, val):
        self.__height = val

    @property
    def height1(self):
        """１段目の箱の縦幅"""
        return self.__height1

    @height1.setter
    def height1(self, val):
        self.__height1 = val

    @property
    def height2(self):
        """２段目の箱の縦幅"""
        return self.__height2

    @height2.setter
    def height2(self, val):
        self.__height2 = val

    @property
    def height3(self):
        """３段目の箱の縦幅"""
        return self.__height3

    @height3.setter
    def height3(self, val):
        self.__height3 = val

    @property
    def one_width(self):
        """バー１本分の幅"""
        return self.__one_width

    @one_width.setter
    def one_width(self, val):
        self.__one_width = val

    @property
    def left(self):
        """箱の左座標"""
        return self.__left

    @left.setter
    def left(self, val):
        self.__left = val

    @property
    def right(self):
        """箱の右座標"""
        return self.__right

    @right.setter
    def right(self, val):
        self.__right = val

    @property
    def bottom(self):
        """箱の底辺座標"""
        return self.__bottom

    @bottom.setter
    def bottom(self, val):
        self.__bottom = val

    @property
    def red_left(self):
        """赤いバーの左座標"""
        return self.__red_left

    @red_left.setter
    def red_left(self, val):
        self.__red_left = val

    @property
    def green_left(self):
        """緑のバーの左座標"""
        return self.__green_left

    @green_left.setter
    def green_left(self, val):
        self.__green_left = val

    @property
    def blue_left(self):
        """青のバーの左座標"""
        return self.__blue_left

    @blue_left.setter
    def blue_left(self, val):
        self.__blue_left = val

    @property
    def rank1_p1(self):
        """１段目の箱の左上点"""
        return self.__rank1_p1

    @rank1_p1.setter
    def rank1_p1(self, val):
        self.__rank1_p1 = val

    @property
    def rank1_p2(self):
        """１段目の箱の右下点"""
        return self.__rank1_p2

    @rank1_p2.setter
    def rank1_p2(self, val):
        self.__rank1_p2 = val

    @property
    def rank2_p1(self):
        """２段目の箱の左上点"""
        return self.__rank2_p1

    @rank2_p1.setter
    def rank2_p1(self, val):
        self.__rank2_p1 = val

    @property
    def rank2_p2(self):
        """２段目の箱の右下点"""
        return self.__rank2_p2

    @rank2_p2.setter
    def rank2_p2(self, val):
        self.__rank2_p2 = val

    @property
    def rank3_p1(self):
        """３段目の箱の左上点"""
        return self.__rank3_p1

    @rank3_p1.setter
    def rank3_p1(self, val):
        self.__rank3_p1 = val

    @property
    def rank3_p2(self):
        """３段目の箱の右下点"""
        return self.__rank3_p2

    @rank3_p2.setter
    def rank3_p2(self, val):
        self.__rank3_p2 = val

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

    @property
    def font_height(self):
        """フォントの縦幅"""
        return self.__font_height

    @font_height.setter
    def font_height(self, val):
        self.__font_height = val

    @property
    def font_scale(self):
        """フォント・サイズの倍率"""
        return self.__font_scale

    @font_scale.setter
    def font_scale(self, val):
        self.__font_scale = val

    @property
    def line_type(self):
        """ラインタイプ"""
        return self.__line_type

    @line_type.setter
    def line_type(self, val):
        self.__line_type = val

    @property
    def font(self):
        """フォント"""
        return self.__font

    @font.setter
    def font(self, val):
        self.__font = val

    @property
    def red_addition(self):
        """R値に加算"""
        return self.__red_addition

    @red_addition.setter
    def red_addition(self, val):
        self.__red_addition = val

    @property
    def green_addition(self):
        """G値に加算"""
        return self.__green_addition

    @green_addition.setter
    def green_addition(self, val):
        self.__green_addition = val

    @property
    def blue_addition(self):
        """B値に加算"""
        return self.__blue_addition

    @blue_addition.setter
    def blue_addition(self, val):
        self.__blue_addition = val

    @property
    def red_height(self):
        """Rバーの縦幅"""
        return self.__red_bar_p2[1] - self.__red_bar_p1[1] + self.__red_addition

    @property
    def green_height(self):
        """Gバーの縦幅"""
        return self.__green_bar_p2[1] - self.__green_bar_p1[1] + self.__green_addition

    @property
    def blue_height(self):
        """Bバーの縦幅"""
        return self.__blue_bar_p2[1] - self.__blue_bar_p1[1] + self.__blue_addition

    def draw_outline(self, canvas):
        """輪郭を描きます"""
        cv2.rectangle(canvas, self.rank1_p1,
                      self.rank3_p2, LIGHT_GRAY, thickness=4)

    def draw_rank2_box(self, canvas):
        """２段目の箱を描きます"""
        cv2.rectangle(canvas, self.rank2_p1,
                      self.rank2_p2, BLACK, thickness=4)

    def draw_rgb_number(self, canvas, color):
        """RGB値テキストを描きます"""

        # R値テキスト
        cv2.putText(canvas,
                    f"{color[0]:02x}",
                    (self.red_bar_p2[0]-self.one_width,
                     self.red_bar_p2[1]+self.font_height),  # x,y
                    self.font,
                    self.font_scale,
                    RED,
                    self.line_type)

        # G値テキスト
        cv2.putText(canvas,
                    f"{color[1]:02x}",
                    (self.green_bar_p2[0]-self.one_width,
                     self.green_bar_p2[1]+self.font_height),  # x,y
                    self.font,
                    self.font_scale,
                    GREEN,
                    self.line_type)

        # B値テキスト
        cv2.putText(canvas,
                    f"{color[2]:02x}",
                    (self.blue_bar_p2[0]-self.one_width,
                     self.blue_bar_p2[1]+self.font_height),  # x,y
                    self.font,
                    self.font_scale,
                    BLUE,
                    self.line_type)

    def draw_bar_rate(self, canvas):
        """バー率を描きます"""
        rate_y = int((self.top1 + self.top2)/2)
        gap = int(self.one_width/2)
        cv2.putText(canvas,
                    f"{self.rates[0]}",
                    (self.right+gap, rate_y),  # x,y
                    self.font,
                    self.font_scale,
                    LIGHT_GRAY,
                    self.line_type)
        rate_y = int((self.top2 + self.top3)/2)
        cv2.putText(canvas,
                    f"{self.rates[1]}",
                    (self.right+gap, rate_y),  # x,y
                    self.font,
                    self.font_scale,
                    BLACK,
                    self.line_type)
        rate_y = int((self.top3 + self.bottom)/2)
        cv2.putText(canvas,
                    f"{self.rates[2]}",
                    (self.right+gap, rate_y),  # x,y
                    self.font,
                    self.font_scale,
                    LIGHT_GRAY,
                    self.line_type)

    def draw_bars(self, canvas):
        """バーを描きます"""
        # バーR
        cv2.rectangle(canvas, (self.red_bar_p1[0], self.red_bar_p1[1]-self.red_addition),  # yは逆さ
                      self.red_bar_p2, RED, thickness=-1)

        # バーG
        cv2.rectangle(canvas, (self.green_bar_p1[0], self.green_bar_p1[1]-self.green_addition),
                      self.green_bar_p2, GREEN, thickness=-1)

        # バーB
        cv2.rectangle(canvas, (self.blue_bar_p1[0], self.blue_bar_p1[1]-self.blue_addition),
                      self.blue_bar_p2, BLUE, thickness=-1)

    def create_color(self):
        """色を作成"""
        return (
            int(self.red_height/self.height*255),
            int(self.green_height/self.height*255),
            int(self.blue_height/self.height*255))
