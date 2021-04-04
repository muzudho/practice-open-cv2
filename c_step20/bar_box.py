"""RGBバーの箱
"""

import cv2
from colors import  \
    BRIGHT_GRAY, RED, GREEN, BLUE, \
    BRIGHT_RED, BRIGHT_GREEN, BRIGHT_BLUE, \
    DARK_GRAYISH_BLACK, DARK_GRAYISH_RED, DARK_GRAYISH_GREEN, DARK_GRAYISH_BLUE, \
    PALE_RED, PALE_GREEN, PALE_BLUE
from color_calc import convert_height_to_byte
from conf import GRID_UNIT
from rectangle import Rectangle


class BarBox():
    """RGBバーの箱
    """

    def __init__(self):
        self.__rates = [0, 0, 0]
        self.__top1 = 0
        self.__left = 0
        self.__right = 0
        self.__bottom = 0
        self.__upper_y = 0
        self.__lower_y = 0
        self.__height = 0
        self.__height1 = 0
        self.__height2 = 0
        self.__height3 = 0
        self.__one_width = 0
        self.__y_axis_label_gap = 0
        self.__rate_text_gap = 0
        self.__red_left = 0
        self.__green_left = 0
        self.__blue_left = 0
        self.__rank2_rect = Rectangle()
        self.__rank3_rect = Rectangle()

        self.__n3bars_rect = (Rectangle(), Rectangle(), Rectangle())

        self.__font_scale = 0
        self.__line_type = 0
        self.__font = None
        self.__thickness = 2

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
    def upper_y(self):
        """２段目の箱の上辺"""
        return self.__upper_y

    @upper_y.setter
    def upper_y(self, val):
        self.__upper_y = val

    @property
    def lower_y(self):
        """３段目の箱の上辺"""
        return self.__lower_y

    @lower_y.setter
    def lower_y(self, val):
        self.__lower_y = val

    @property
    def width(self):
        """横幅"""
        return self.__right - self.__left

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
    def y_axis_label_gap(self):
        """箱の右と、Y軸ラベルの間隔"""
        return self.__y_axis_label_gap

    @y_axis_label_gap.setter
    def y_axis_label_gap(self, val):
        self.__y_axis_label_gap = val

    @property
    def rate_text_gap(self):
        """バー率テキストの間隔"""
        return self.__rate_text_gap

    @rate_text_gap.setter
    def rate_text_gap(self, val):
        self.__rate_text_gap = val

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
    def rank1_rect(self):
        """１段目の箱の矩形"""
        return Rectangle(self.__left, self.__top1, self.__right, self.__bottom)

    @property
    def rank2_rect(self):
        """２段目の箱の矩形"""
        return self.__rank2_rect

    @rank2_rect.setter
    def rank2_rect(self, val):
        self.__rank2_rect = val

    @property
    def rank3_rect(self):
        """３段目の箱の矩形"""
        return self.__rank3_rect

    @rank3_rect.setter
    def rank3_rect(self, val):
        self.__rank3_rect = val

    @property
    def n3bars_rect(self):
        """３本のバーの矩形"""
        return self.__n3bars_rect

    @n3bars_rect.setter
    def n3bars_rect(self, val):
        self.__n3bars_rect = val

    @property
    def red_top(self):
        """フィット後の赤バーの上端"""
        return self.__n3bars_rect[0].left_top[1]

    @property
    def green_top(self):
        """フィット後の緑バーの上端"""
        return self.__n3bars_rect[1].left_top[1]

    @property
    def blue_top(self):
        """フィット後の青バーの上端"""
        return self.__n3bars_rect[2].left_top[1]

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
    def thickness(self):
        """線の太さ"""
        return self.__thickness

    def create_rank23d_3bars_height(self):
        """バーの長さを作成"""
        return (
            self.bottom - self.red_top,
            self.bottom - self.green_top,
            self.bottom - self.blue_top)

    def draw_outline(self, canvas):
        """輪郭を描きます"""
        cv2.rectangle(
            canvas,
            self.rank1_rect.left_top,
            self.rank3_rect.right_bottom,
            BRIGHT_GRAY,
            thickness=self.thickness)

    def draw_rank2_box(self, canvas):
        """２段目の箱の輪郭を描きます"""
        # 線の太さを考慮
        thickness_minus1 = self.thickness-1
        cv2.rectangle(
            canvas,
            (self.rank2_rect.left_top[0]-thickness_minus1,
             self.rank2_rect.left_top[1]-thickness_minus1),
            (self.rank2_rect.right_bottom[0]+thickness_minus1,
             self.rank2_rect.right_bottom[1]+thickness_minus1),
            DARK_GRAYISH_BLACK,
            thickness=thickness_minus1+1)

    def draw_3figures(self, canvas, num, left, top, color):
        """３桁の数字の描画"""
        def parse_figures(num):
            if num > 99:
                return [f"{int(num/100)}", f"{int(num/10) % 10}", f"{num % 10}"]
            if num > 9:
                return ["", f"{int(num/10) % 10}", f"{num % 10}"]
            if num > -1:
                return ["", f"", f"{num % 10}"]
            if num > -10:
                return ["", f"-", f"{num % 10}"]
            if num > -100:
                return ["-", f"{int(num/10) % 10}", f"{num % 10}"]
            # 入りきらない
            return ["X", "X", f"X"]
        figures = parse_figures(num)
        for i, figure in enumerate(figures):
            cv2.putText(canvas,
                        f"{figure}",
                        (int(left+i*0.7*GRID_UNIT), top),  # x,y
                        self.font,
                        self.font_scale,
                        color,
                        self.line_type)

    def draw_rgb_number(self, canvas, rank23d_color):
        """RGB値テキストを描きます"""
        top2_byte = convert_height_to_byte(
            self.height2+self.height3, self.height)
        top3_byte = convert_height_to_byte(
            self.height3, self.height)
        top2_over_top = int(self.upper_y-GRID_UNIT/2)

        # 10進R値テキスト
        color = rank23d_color[0]
        font_color = DARK_GRAYISH_RED
        if color == top2_byte:
            top = top2_over_top
        elif color == top3_byte:
            top = self.red_top + GRID_UNIT
        else:
            top = self.red_top + GRID_UNIT
            font_color = PALE_RED

        self.draw_3figures(
            canvas,
            color,
            self.__red_left,
            top,
            font_color)

        # 10進G値テキスト
        color = rank23d_color[1]
        font_color = DARK_GRAYISH_GREEN
        if color == top2_byte:
            top = top2_over_top
        elif color == top3_byte:
            top = self.green_top + GRID_UNIT
        else:
            top = self.green_top + GRID_UNIT
            font_color = PALE_GREEN

        self.draw_3figures(
            canvas,
            color,
            self.__green_left,
            top,
            font_color)

        # 10進B値テキスト
        color = rank23d_color[2]
        font_color = DARK_GRAYISH_BLUE
        if color == top2_byte:
            top = top2_over_top
        elif color == top3_byte:
            top = self.blue_top + GRID_UNIT
        else:
            top = self.blue_top + GRID_UNIT
            font_color = PALE_BLUE

        self.draw_3figures(
            canvas,
            color,
            self.__blue_left,
            top,
            font_color)

    def draw_y_axis_label(self, canvas):
        """Y軸のラベルを描きます"""
        rank23_byte = convert_height_to_byte(
            self.height2+self.height3, self.height)
        rank3_byte = convert_height_to_byte(
            self.height3, self.height)

        left = self.right+self.y_axis_label_gap
        # 255
        self.draw_3figures(
            canvas, 255, left, int(self.top1-GRID_UNIT/2), BRIGHT_GRAY)
        # 0
        self.draw_3figures(
            canvas, 0, left, int(self.bottom+GRID_UNIT), BRIGHT_GRAY)
        # ceil
        self.draw_3figures(
            canvas, rank23_byte, left, int(self.upper_y-GRID_UNIT/2), DARK_GRAYISH_BLACK)
        # base_line
        self.draw_3figures(
            canvas, rank3_byte, left, int(self.lower_y+GRID_UNIT), DARK_GRAYISH_BLACK)

    def draw_bars_rate(self, canvas):
        """バー率を描きます"""
        # １段目のバー率
        rate_y = int((self.top1 + self.upper_y)/2 - GRID_UNIT/2)
        cv2.putText(canvas,
                    f"{int(self.rates[0]*100):3}%",
                    (self.right+self.rate_text_gap, rate_y),  # x,y
                    self.font,
                    self.font_scale,
                    BRIGHT_GRAY,
                    self.line_type)
        # ２段目のバー率
        rate_y = int((self.upper_y + self.lower_y)/2 + GRID_UNIT/2)
        cv2.putText(canvas,
                    f"{int(self.rates[1]*100):3}%",
                    (self.right+self.rate_text_gap, rate_y),  # x,y
                    self.font,
                    self.font_scale,
                    DARK_GRAYISH_BLACK,
                    self.line_type)
        # ３段目のバー率
        rate_y = int((self.lower_y + self.bottom)/2 + GRID_UNIT/2)
        cv2.putText(canvas,
                    f"{int(self.rates[2]*100):3}%",
                    (self.right+self.rate_text_gap, rate_y),  # x,y
                    self.font,
                    self.font_scale,
                    BRIGHT_GRAY,
                    self.line_type)

    def draw_3bars(self, canvas):
        """バーを描きます"""

        # yは逆さ

        # バーR
        left = self.__red_left
        right = left + self.__one_width
        top = self.red_top
        bottom = self.lower_y
        # print(
        #    f"left={left} top={top} right={right} bottom={bottom} \
        # RED=({RED[0]}, {RED[1]}, {RED[2]})")
        cv2.rectangle(canvas,
                      (left, self.lower_y),
                      (right, self.bottom),
                      BRIGHT_RED,
                      thickness=-1)  # rank3
        cv2.rectangle(canvas,
                      (left, top),
                      (right, bottom),
                      RED,
                      thickness=-1)  # rank2d

        # バーG
        left = self.__green_left
        right = left + self.__one_width
        top = self.green_top
        cv2.rectangle(canvas,
                      (left, self.lower_y),
                      (right, self.bottom),
                      BRIGHT_GREEN,
                      thickness=-1)
        cv2.rectangle(canvas,
                      (left, top),
                      (right, self.lower_y),
                      GREEN,
                      thickness=-1)

        # バーB
        left = self.__blue_left
        right = left + self.__one_width
        top = self.blue_top
        cv2.rectangle(canvas,
                      (left, self.lower_y),
                      (right, self.bottom),
                      BRIGHT_BLUE, thickness=-1)
        cv2.rectangle(canvas,
                      (left, top),
                      (right, self.lower_y),
                      BLUE, thickness=-1)
