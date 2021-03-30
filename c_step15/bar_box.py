"""RGBバーの箱
"""

import cv2
from colors import BLACK, WHITE, \
    BRIGHT_GRAY, RED, GREEN, BLUE
from color_calc import convert_height_to_byte, convert_byte_to_height
from conf import GRID_UNIT
from rectangle import Rectangle


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
        self.__y_axis_label_gap = 0
        self.__rate_text_gap = 0
        self.__left = 0
        self.__right = 0
        self.__bottom = 0
        self.__red_left = 0
        self.__red2_left = 0
        self.__green_left = 0
        self.__green2_left = 0
        self.__blue_left = 0
        self.__blue2_left = 0
        self.__rank1_rect = Rectangle()
        self.__rank2_rect = Rectangle()
        self.__rank3_rect = Rectangle()

        self.__step1_rect = (Rectangle(), Rectangle(), Rectangle())

        self.__font_scale = 0
        self.__line_type = 0
        self.__font = None
        self.__delta_3bars_height = (0, 0, 0)
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
    def red2_left(self):
        """赤いバーの左座標"""
        return self.__red2_left

    @red2_left.setter
    def red2_left(self, val):
        self.__red2_left = val

    @property
    def green_left(self):
        """緑のバーの左座標"""
        return self.__green_left

    @green_left.setter
    def green_left(self, val):
        self.__green_left = val

    @property
    def green2_left(self):
        """緑のバーの左座標"""
        return self.__green2_left

    @green2_left.setter
    def green2_left(self, val):
        self.__green2_left = val

    @property
    def blue_left(self):
        """青のバーの左座標"""
        return self.__blue_left

    @blue_left.setter
    def blue_left(self, val):
        self.__blue_left = val

    @property
    def blue2_left(self):
        """青のバーの左座標"""
        return self.__blue2_left

    @blue2_left.setter
    def blue2_left(self, val):
        self.__blue2_left = val

    @property
    def rank1_rect(self):
        """１段目の箱の矩形"""
        return self.__rank1_rect

    @rank1_rect.setter
    def rank1_rect(self, val):
        self.__rank1_rect = val

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
    def step1_rect(self):
        """step1の３本のバーの矩形"""
        return self.__step1_rect

    @step1_rect.setter
    def step1_rect(self, val):
        self.__step1_rect = val

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
    def delta_3bars_height(self):
        """色の追加値"""
        return self.__delta_3bars_height

    @delta_3bars_height.setter
    def delta_3bars_height(self, val):
        self.__delta_3bars_height = val

    @property
    def thickness(self):
        """線の太さ"""
        return self.__thickness

    def create_step1_3bars_height(self):
        """色を作成"""
        return (
            self.__step1_rect[0].right_bottom[1] -
            self.__step1_rect[0].left_top[1],
            self.__step1_rect[1].right_bottom[1] -
            self.__step1_rect[1].left_top[1],
            self.__step1_rect[2].right_bottom[1] - self.__step1_rect[2].left_top[1])

    def create_rank23_3bars_height(self):
        """色を作成"""
        rank2_height = self.create_step1_3bars_height()
        return (
            rank2_height[0] + self.height3,
            rank2_height[1] + self.height3,
            rank2_height[2] + self.height3)

    def create_rank23a_3bars_height(self):
        """色を作成"""
        rank23_height = self.create_rank23_3bars_height()
        return (
            rank23_height[0] + self.delta_3bars_height[0],
            rank23_height[1] + self.delta_3bars_height[1],
            rank23_height[2] + self.delta_3bars_height[2])

    def get_max_rank23_height(self):
        """追加部分を含まない、最長のバーの縦幅"""
        rank23_height = self.create_rank23_3bars_height()
        return max(rank23_height[0], rank23_height[1], rank23_height[2])

    def get_min_rank23_height(self):
        """追加部分を含まない、最短のバーの縦幅"""
        rank23_height = self.create_rank23_3bars_height()
        return min(rank23_height[0], rank23_height[1], rank23_height[2])

    def get_max_step1_height(self):
        """追加部分と、３段目を含まない、最長のバーの縦幅"""
        step1_height = self.create_step1_3bars_height()
        return max(step1_height[0], step1_height[1], step1_height[2])

    def draw_outline(self, canvas):
        """輪郭を描きます"""
        cv2.rectangle(
            canvas,
            self.rank1_rect.left_top,
            self.rank3_rect.right_bottom,
            BRIGHT_GRAY,
            thickness=self.thickness)

    def draw_rank2_box(self, canvas):
        """２段目の箱を描きます"""
        # 線の太さを考慮
        thickness_minus1 = self.thickness-1
        cv2.rectangle(
            canvas,
            (self.rank2_rect.left_top[0]-thickness_minus1,
             self.rank2_rect.left_top[1]-thickness_minus1),
            (self.rank2_rect.right_bottom[0]+thickness_minus1,
             self.rank2_rect.right_bottom[1]+thickness_minus1),
            BLACK,
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

    def draw_rgb_number(self, canvas,
                        step1_color,
                        rank3_byte,
                        rank23d_color):
        """RGB値テキストを描きます"""

        # 10進R値テキスト
        top = self.bottom + GRID_UNIT

        # Red
        self.draw_3figures(
            canvas,
            step1_color[0] + rank3_byte + rank23d_color[0],
            self.step1_rect[0].left_top[0],
            top,
            RED)

        # 10進G値テキスト
        self.draw_3figures(
            canvas,
            step1_color[1] + rank3_byte + rank23d_color[1],
            self.step1_rect[1].left_top[0],
            top,
            GREEN)

        # 10進B値テキスト
        self.draw_3figures(
            canvas,
            step1_color[2] + rank3_byte + rank23d_color[2],
            self.step1_rect[2].left_top[0],
            top,
            BLUE)

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
        # ceil
        self.draw_3figures(
            canvas, rank23_byte, left, int(self.top2-GRID_UNIT/2), BLACK)
        # base_line
        self.draw_3figures(
            canvas, rank3_byte, left, int(self.top3+GRID_UNIT), BLACK)
        # 0
        self.draw_3figures(
            canvas, 0, left, int(self.bottom+GRID_UNIT), BRIGHT_GRAY)

    def draw_bars_rate(self, canvas):
        """バー率を描きます"""
        # １段目のバー率
        rate_y = int((self.top1 + self.top2)/2 - GRID_UNIT/2)
        cv2.putText(canvas,
                    f"{int(self.rates[0]*100):3}%",
                    (self.right+self.rate_text_gap, rate_y),  # x,y
                    self.font,
                    self.font_scale,
                    BRIGHT_GRAY,
                    self.line_type)
        # ２段目のバー率
        rate_y = int((self.top2 + self.top3)/2 + GRID_UNIT/2)
        cv2.putText(canvas,
                    f"{int(self.rates[1]*100):3}%",
                    (self.right+self.rate_text_gap, rate_y),  # x,y
                    self.font,
                    self.font_scale,
                    BLACK,
                    self.line_type)
        # ３段目のバー率
        rate_y = int((self.top3 + self.bottom)/2 + GRID_UNIT/2)
        cv2.putText(canvas,
                    f"{int(self.rates[2]*100):3}%",
                    (self.right+self.rate_text_gap, rate_y),  # x,y
                    self.font,
                    self.font_scale,
                    BRIGHT_GRAY,
                    self.line_type)

    def draw_3bars(self, canvas, delta_color, step1_color, rank3_color):
        """バーを描きます"""

        # yは逆さ

        # バーR
        left = self.step1_rect[0].left_top[0]
        right = self.step1_rect[0].right_bottom[0]
        top2 = self.step1_rect[0].left_top[1]
        cv2.rectangle(canvas, (left, top2),
                      self.step1_rect[0].right_bottom, step1_color[0], thickness=-1)  # step1
        cv2.rectangle(canvas, (left, self.top3),
                      (right, self.bottom),
                      rank3_color[0], thickness=-1)  # rank3
        delta = self.delta_3bars_height[0]
        if delta > 0:
            delta_top = top2-delta
            delta_bottom = top2
        else:
            delta_top = top2
            delta_bottom = top2-delta
        cv2.rectangle(canvas,
                      (left+self.one_width, delta_top),
                      (right+self.one_width, delta_bottom),
                      delta_color[0],
                      thickness=-1)  # delta

        # バーG
        left = self.step1_rect[1].left_top[0]
        right = self.step1_rect[1].right_bottom[0]
        top2 = self.step1_rect[1].left_top[1]
        cv2.rectangle(canvas, (left, top2),
                      self.step1_rect[1].right_bottom, step1_color[1], thickness=-1)
        cv2.rectangle(canvas, (left, self.top3),
                      (right,
                       self.bottom), rank3_color[1], thickness=-1)
        delta = self.delta_3bars_height[1]
        if delta > 0:
            delta_top = top2-delta
            delta_bottom = top2
        else:
            delta_top = top2
            delta_bottom = top2-delta
        cv2.rectangle(canvas,
                      (left+self.one_width, delta_top),
                      (right+self.one_width, delta_bottom),
                      delta_color[1],
                      thickness=-1)

        # バーB
        left = self.step1_rect[2].left_top[0]
        right = self.step1_rect[2].right_bottom[0]
        top2 = self.step1_rect[2].left_top[1]
        cv2.rectangle(canvas,
                      (left, top2),
                      self.step1_rect[2].right_bottom,
                      step1_color[2],
                      thickness=-1)
        cv2.rectangle(canvas,
                      (left, self.top3),
                      (right, self.bottom),
                      rank3_color[2],
                      thickness=-1)
        delta = self.delta_3bars_height[2]
        if delta > 0:
            delta_top = top2-delta
            delta_bottom = top2
        else:
            delta_top = top2
            delta_bottom = top2-delta
        cv2.rectangle(canvas,
                      (left+self.one_width, delta_top),
                      (right+self.one_width, delta_bottom),
                      delta_color[2],
                      thickness=-1)
