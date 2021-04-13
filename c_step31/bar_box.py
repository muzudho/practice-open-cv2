"""RGBバーの箱
"""

import cv2
from colors import  \
    BRIGHT_GRAY, SOFT_RED, SOFT_GREEN, SOFT_BLUE, \
    DARK_GRAYISH_GRAY, DARK_GRAYISH_RED, DARK_GRAYISH_GREEN, DARK_GRAYISH_BLUE, \
    PALE_RED, PALE_GREEN, PALE_BLUE
from color_calc import convert_pixel_to_color_element
from conf import GRID_UNIT, BAR_TICKS  # , DE_GAMMA_FROM_LINEAR
from rectangle import Rectangle
from cv2_helper import color_for_cv2, point_for_cv2
# from gamma_correction import de_gamma_from_linear_x


class BarBox():
    """RGBバーの箱
    """

    def __init__(self):
        self.__rates = [0, 0, 0]
        self.__top = 0
        self.__left = 0
        self.__right = 0
        self.__bottom = 0
        self.__upper_x = 0
        self.__lower_x = 0
        self.__label_gap = 0

        self.__red_right = 0
        self.__green_right = 0
        self.__blue_right = 0

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
    def top(self):
        """１段目の箱の上辺"""
        return self.__top

    @top.setter
    def top(self, val):
        self.__top = val

    @property
    def upper_x(self):
        """上限値(U)"""
        return self.__upper_x

    @upper_x.setter
    def upper_x(self, val):
        self.__upper_x = val

    @property
    def lower_x(self):
        """下限値(L)"""
        return self.__lower_x

    @lower_x.setter
    def lower_x(self, val):
        self.__lower_x = val

    @property
    def width(self):
        """横幅"""
        return self.__right - self.__left

    @property
    def height(self):
        """箱の縦幅"""
        return self.__bottom - self.__top  # yは逆さ

    @property
    def one_height(self):
        """バー１本分の縦幅 (float)"""
        return (self.__bottom - self.__top) / 3  # yは逆さ

    @property
    def label_gap(self):
        """箱の右と、Y軸ラベルの間隔"""
        return self.__label_gap

    @label_gap.setter
    def label_gap(self, val):
        self.__label_gap = val

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
    def red_right(self):
        """赤バーの右端"""
        return self.__red_right

    @red_right.setter
    def red_right(self, val):
        self.__red_right = val

    @property
    def red_top(self):
        """赤いバーの上端"""
        return self.top

    @property
    def green_right(self):
        """緑バーの右端"""
        return self.__green_right

    @green_right.setter
    def green_right(self, val):
        self.__green_right = val

    @property
    def green_top(self):
        """緑のバー上端"""
        return self.top + self.one_height

    @property
    def blue_right(self):
        """青バーの右端"""
        return self.__blue_right

    @blue_right.setter
    def blue_right(self, val):
        self.__blue_right = val

    @property
    def blue_top(self):
        """青のバーの上端"""
        return self.top + 2*self.one_height

    @property
    def rank1_rect(self):
        """１段目の箱の矩形"""
        return Rectangle(self.__left, self.__top, self.__right, self.__bottom)

    @property
    def rank2_rect(self):
        """２段目の箱の矩形"""
        return Rectangle(self.__lower_x, self.__top, self.__upper_x, self.__bottom)

    @property
    def rank3_rect(self):
        """３段目の箱の矩形"""
        return Rectangle(self.__upper_x, self.__top, self.__right, self.__bottom)

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

    def create_3bars_width(self):
        """バーの長さを作成"""
        return (
            self.red_right - self.__left,
            self.green_right - self.__left,
            self.blue_right - self.__left)

    def draw_outline(self, canvas):
        """輪郭を描きます"""
        cv2.rectangle(
            canvas,
            point_for_cv2((self.__left, self.__top)),
            point_for_cv2((self.__right, self.__bottom)),
            color_for_cv2(BRIGHT_GRAY),
            thickness=self.thickness)

    def draw_rank2_box(self, canvas):
        """２段目の箱の輪郭を描きます"""
        # 線の太さを考慮
        thickness_minus1 = self.thickness-1
        cv2.rectangle(
            canvas,
            point_for_cv2((self.__lower_x - thickness_minus1,
                           self.__top - thickness_minus1)),
            point_for_cv2((self.__upper_x + thickness_minus1,
                           self.__bottom + thickness_minus1)),
            color_for_cv2(DARK_GRAYISH_GRAY),
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
                        point_for_cv2((left+i*0.7*GRID_UNIT, top)),  # x,y
                        self.font,
                        self.font_scale,
                        color_for_cv2(color),
                        self.line_type)

    def draw_rgb_number(self, canvas, rgb_numbers):
        """RGB値テキストを描きます"""
        center_box_width = self.__upper_x - self.__lower_x
        left_box_width = self.__lower_x - self.__left
        upper_color_element = round(BAR_TICKS * convert_pixel_to_color_element(
            center_box_width+left_box_width, self.width))
        lower_color_element = round(BAR_TICKS * convert_pixel_to_color_element(
            left_box_width, self.width))
        upper_x_over = self.__upper_x+GRID_UNIT/2
        lower_x_over = self.__lower_x-2.5*GRID_UNIT

        # 色成分値
        red_num = round(BAR_TICKS * rgb_numbers[0])
        green_num = round(BAR_TICKS * rgb_numbers[1])
        blue_num = round(BAR_TICKS * rgb_numbers[2])

        # 10進R値テキスト
        font_color = DARK_GRAYISH_RED
        if red_num == upper_color_element:
            left = upper_x_over
            font_color = DARK_GRAYISH_GRAY
        elif red_num == lower_color_element:
            left = lower_x_over
            font_color = DARK_GRAYISH_GRAY
        else:
            left = self.red_right - 2.5*GRID_UNIT
            font_color = PALE_RED

        self.draw_3figures(
            canvas,
            round(red_num),
            left,
            self.red_top+1.5*GRID_UNIT,
            font_color)

        # 10進G値テキスト
        font_color = DARK_GRAYISH_GREEN
        if green_num == upper_color_element:
            left = upper_x_over
            font_color = DARK_GRAYISH_GRAY
        elif green_num == lower_color_element:
            left = lower_x_over
            font_color = DARK_GRAYISH_GRAY
        else:
            left = self.green_right - 2.5*GRID_UNIT
            font_color = PALE_GREEN

        self.draw_3figures(
            canvas,
            round(green_num),
            left,
            self.green_top+1.5*GRID_UNIT,
            font_color)

        # 10進B値テキスト
        font_color = DARK_GRAYISH_BLUE
        if blue_num == upper_color_element:
            left = upper_x_over
            font_color = DARK_GRAYISH_GRAY
        elif blue_num == lower_color_element:
            left = lower_x_over
            font_color = DARK_GRAYISH_GRAY
        else:
            left = self.blue_right - 2.5*GRID_UNIT
            font_color = PALE_BLUE

        self.draw_3figures(
            canvas,
            round(blue_num),
            left,
            self.blue_top+1.5*GRID_UNIT,
            font_color)

    def draw_x_axis_label(self, canvas):
        """X軸のラベルを描きます"""
        center_box_width = self.__upper_x - self.__lower_x
        left_box_width = self.__lower_x - self.__left

        # 各数値
        max_val = BAR_TICKS-1
        zero = 0
        upper_color_element = convert_pixel_to_color_element(
            center_box_width+left_box_width, self.width)
        lower_color_element = convert_pixel_to_color_element(
            left_box_width, self.width)

        # if DE_GAMMA_FROM_LINEAR:
        #    max_val = de_gamma_from_linear_x(max_val)
        #    zero = de_gamma_from_linear_x(zero)
        #    upper_color_element = de_gamma_from_linear_x(upper_color_element)
        #    lower_color_element = de_gamma_from_linear_x(lower_color_element)

        top = self.top+self.label_gap
        # バーの最大値(0から始まる数)
        self.draw_3figures(
            canvas,
            round(max_val),
            self.right+GRID_UNIT/2,
            top,
            BRIGHT_GRAY)
        # 0
        self.draw_3figures(
            canvas,
            round(zero),
            self.left-2.5*GRID_UNIT,
            top,
            BRIGHT_GRAY)
        # U
        self.draw_3figures(
            canvas,
            round(BAR_TICKS * upper_color_element),
            self.upper_x+GRID_UNIT/2,
            top,
            DARK_GRAYISH_GRAY)
        # L
        self.draw_3figures(
            canvas,
            round(BAR_TICKS * lower_color_element),
            self.lower_x-2.5*GRID_UNIT,
            top,
            DARK_GRAYISH_GRAY)

    def draw_bars_rate(self, canvas):
        """バー率を描きます"""

        # 各数値
        left_box_rate = self.rates[0]
        center_box_rate = self.rates[1]
        right_box_rate = self.rates[2]

        # if DE_GAMMA_FROM_LINEAR:
        #    left_box_rate = de_gamma_from_linear_x(left_box_rate)
        #    center_box_rate = de_gamma_from_linear_x(center_box_rate)
        #    right_box_rate = de_gamma_from_linear_x(right_box_rate)

        top = self.top+self.label_gap
        # 左列のバー率
        left = self.__left - 3*GRID_UNIT
        cv2.putText(canvas,
                    f"{int(left_box_rate*100):3}%",
                    point_for_cv2((left, top)),  # x,y
                    self.font,
                    self.font_scale,
                    color_for_cv2(BRIGHT_GRAY),
                    self.line_type)
        # 中列のバー率
        left = (self.__lower_x + self.__upper_x)/2 - 1.5*GRID_UNIT
        cv2.putText(canvas,
                    f"{int(center_box_rate*100):3}%",
                    point_for_cv2((left, top)),  # x,y
                    self.font,
                    self.font_scale,
                    color_for_cv2(DARK_GRAYISH_GRAY),
                    self.line_type)
        # 右列のバー率
        left = self.__right - 0.5*GRID_UNIT
        cv2.putText(canvas,
                    f"{int(right_box_rate*100):3}%",
                    point_for_cv2((left, top)),  # x,y
                    self.font,
                    self.font_scale,
                    color_for_cv2(BRIGHT_GRAY),
                    self.line_type)

    def draw_3bars(self, canvas):
        """バーを描きます"""

        # yは逆さ

        # バーR
        cv2.rectangle(canvas,
                      point_for_cv2((self.__left, self.__top)),
                      point_for_cv2((self.__red_right,
                                     self.__top + self.one_height)),
                      color_for_cv2(SOFT_RED),
                      thickness=-1)

        # バーG
        cv2.rectangle(canvas,
                      point_for_cv2(
                          (self.__left, self.__top + self.one_height)),
                      point_for_cv2((self.__green_right,
                                     self.__top + 2*self.one_height)),
                      color_for_cv2(SOFT_GREEN),
                      thickness=-1)

        # バーB
        cv2.rectangle(canvas,
                      point_for_cv2((self.__left, self.__top +
                                     2*self.one_height)),
                      point_for_cv2((self.__blue_right, self.__bottom)),
                      color_for_cv2(SOFT_BLUE),
                      thickness=-1)
