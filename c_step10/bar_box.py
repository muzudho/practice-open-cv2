"""RGBバーの箱
"""

import cv2
from colors import LIGHT_GRAY, BLACK
from conf import GRID_INTERVAL_H
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
        self.__rate_text_gap = 0
        self.__left = 0
        self.__right = 0
        self.__bottom = 0
        self.__red_left = 0
        self.__green_left = 0
        self.__blue_left = 0
        self.__rank1_rect = Rectangle()
        self.__rank2_rect = Rectangle()
        self.__rank3_rect = Rectangle()

        self.__step1_red_bar_rect = Rectangle()
        self.__step1_green_bar_rect = Rectangle()
        self.__step1_blue_bar_rect = Rectangle()

        self.__font_scale = 0
        self.__line_type = 0
        self.__font = None
        self.__addition_3bars_height = (0, 0, 0)
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
    def step1_red_bar_rect(self):
        """step1赤バーの矩形"""
        return self.__step1_red_bar_rect

    @step1_red_bar_rect.setter
    def step1_red_bar_rect(self, val):
        self.__step1_red_bar_rect = val

    @property
    def step1_green_bar_rect(self):
        """step1緑バーの矩形"""
        return self.__step1_green_bar_rect

    @step1_green_bar_rect.setter
    def step1_green_bar_rect(self, val):
        self.__step1_green_bar_rect = val

    @property
    def step1_blue_bar_rect(self):
        """step1青バーの矩形"""
        return self.__step1_blue_bar_rect

    @step1_blue_bar_rect.setter
    def step1_blue_bar_rect(self, val):
        self.__step1_blue_bar_rect = val

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
    def addition_3bars_height(self):
        """色の追加値"""
        return self.__addition_3bars_height

    @addition_3bars_height.setter
    def addition_3bars_height(self, val):
        self.__addition_3bars_height = val

    @property
    def thickness(self):
        """線の太さ"""
        return self.__thickness

    def create_step1_3bars_height(self):
        """色を作成"""
        return (
            self.__step1_red_bar_rect.right_bottom[1] -
            self.__step1_red_bar_rect.left_top[1],
            self.__step1_green_bar_rect.right_bottom[1] -
            self.__step1_green_bar_rect.left_top[1],
            self.__step1_blue_bar_rect.right_bottom[1] - self.__step1_blue_bar_rect.left_top[1])

    def create_rank3_3bars_height(self):
        """色を作成"""
        return (
            self.bottom - self.__rank3_rect.left_top[1],
            self.bottom - self.__rank3_rect.left_top[1],
            self.bottom - self.__rank3_rect.left_top[1])

    def create_rank23_3bars_height(self):
        """色を作成"""
        return (
            self.bottom - self.__step1_red_bar_rect.left_top[1],
            self.bottom - self.__step1_green_bar_rect.left_top[1],
            self.bottom - self.__step1_blue_bar_rect.left_top[1])

    def create_rank23a_3bars_height(self):
        """色を作成"""
        return (
            self.bottom -
            self.__step1_red_bar_rect.left_top[1] +
            self.addition_3bars_height[0],
            self.bottom -
            self.__step1_green_bar_rect.left_top[1] +
            self.addition_3bars_height[1],
            self.bottom - self.__step1_blue_bar_rect.left_top[1] + self.addition_3bars_height[2])

    @property
    def rank1_height_as_byte(self):
        """１段目が colorの成分値として いくつか"""
        return int(255 * (self.height1 / self.height))

    @property
    def rank3_height_as_byte(self):
        """３段目が colorの成分値として いくつか"""
        return int(255 * (self.height3 / self.height))

    def get_step1_upper_bound_y(self):
        """step1の上限の座標"""
        return min(
            self.step1_red_bar_rect.left_top[1],
            self.step1_green_bar_rect.left_top[1],
            self.step1_blue_bar_rect.left_top[1])

    def draw_outline(self, canvas):
        """輪郭を描きます"""
        cv2.rectangle(
            canvas,
            self.rank1_rect.left_top,
            self.rank3_rect.right_bottom,
            LIGHT_GRAY,
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

    def draw_rgb_number(self, canvas,
                        a_color, a_3colors,
                        step1_color, step1_3colors,
                        rank3_color, rank3_3colors,
                        rank23a_color, rank23a_3colors):
        """RGB値テキストを描きます"""

        top = self.bottom+int(4*GRID_INTERVAL_H)

        def parse_figures(num):
            if num > 99:
                return [f"{int(num/100)}", f"{int(num/10) % 10}", f"{num % 10}"]
            if num > 10:
                return ["", f"{int(num/10) % 10}", f"{num % 10}"]
            return ["", "", f"{num % 10}"]

            # 1段目 10進R値テキスト
        if a_color[0] != 0:
            figures = parse_figures(a_color[0])
            for i, figure in enumerate(figures):
                cv2.putText(canvas,
                            f"{figure}",
                            (self.step1_red_bar_rect.left_top[0]+i*2*GRID_INTERVAL_H,
                             top),  # x,y
                            self.font,
                            self.font_scale,
                            a_3colors[0],
                            self.line_type)

        # 1段目 10進G値テキスト
        if a_color[1] != 0:
            figures = parse_figures(a_color[1])
            for i, figure in enumerate(figures):
                cv2.putText(canvas,
                            f"{figure}",
                            (self.step1_green_bar_rect.left_top[0]+i*2*GRID_INTERVAL_H,
                             top),  # x,y
                            self.font,
                            self.font_scale,
                            a_3colors[1],
                            self.line_type)

        # 1段目 10進B値テキスト
        if a_color[2] != 0:
            figures = parse_figures(a_color[2])
            for i, figure in enumerate(figures):
                cv2.putText(canvas,
                            f"{figure}",
                            (self.step1_blue_bar_rect.left_top[0]+i*2*GRID_INTERVAL_H,
                             top),  # x,y
                            self.font,
                            self.font_scale,
                            a_3colors[2],
                            self.line_type)

        top = self.bottom+int(8*GRID_INTERVAL_H)

        # 2段目 10進R値テキスト
        if step1_color[0] != 0:
            figures = parse_figures(step1_color[0])
            for i, figure in enumerate(figures):
                cv2.putText(canvas,
                            f"{figure}",
                            (self.step1_red_bar_rect.left_top[0]+i*2*GRID_INTERVAL_H,
                             top),  # x,y
                            self.font,
                            self.font_scale,
                            step1_3colors[0],
                            self.line_type)

        # 2段目 10進G値テキスト
        if step1_color[1] != 0:
            figures = parse_figures(step1_color[1])
            for i, figure in enumerate(figures):
                cv2.putText(canvas,
                            f"{figure}",
                            (self.step1_green_bar_rect.left_top[0]+i*2*GRID_INTERVAL_H,
                             top),  # x,y
                            self.font,
                            self.font_scale,
                            step1_3colors[1],
                            self.line_type)

        # 2段目 10進B値テキスト
        if step1_color[2] != 0:
            figures = parse_figures(step1_color[2])
            for i, figure in enumerate(figures):
                cv2.putText(canvas,
                            f"{figure}",
                            (self.step1_blue_bar_rect.left_top[0]+i*2*GRID_INTERVAL_H,
                             top),  # x,y
                            self.font,
                            self.font_scale,
                            step1_3colors[2],
                            self.line_type)

        top = self.bottom+int(12*GRID_INTERVAL_H)

        # 3段目 10進R値テキスト
        if rank3_color[0] != 0:
            figures = parse_figures(rank3_color[0])
            for i, figure in enumerate(figures):
                cv2.putText(canvas,
                            f"{figure}",
                            (self.step1_red_bar_rect.left_top[0]+i*2*GRID_INTERVAL_H,
                             top),  # x,y
                            self.font,
                            self.font_scale,
                            rank3_3colors[0],
                            self.line_type)

        # 3段目 10進G値テキスト
        if rank3_color[1] != 0:
            figures = parse_figures(rank3_color[1])
            for i, figure in enumerate(figures):
                cv2.putText(canvas,
                            f"{figure}",
                            (self.step1_green_bar_rect.left_top[0]+i*2*GRID_INTERVAL_H,
                             top),  # x,y
                            self.font,
                            self.font_scale,
                            rank3_3colors[1],
                            self.line_type)

        # 3段目 10進B値テキスト
        if rank3_color[2] != 0:
            figures = parse_figures(rank3_color[2])
            for i, figure in enumerate(figures):
                cv2.putText(canvas,
                            f"{figure}",
                            (self.step1_blue_bar_rect.left_top[0]+i*2*GRID_INTERVAL_H,
                             top),  # x,y
                            self.font,
                            self.font_scale,
                            rank3_3colors[2],
                            self.line_type)

        top = self.bottom+int(17*GRID_INTERVAL_H)

        # 4段目 10進R値テキスト
        figures = parse_figures(rank23a_color[0])
        for i, figure in enumerate(figures):
            cv2.putText(canvas,
                        f"{figure}",
                        (self.step1_red_bar_rect.left_top[0]+i*2*GRID_INTERVAL_H,
                         top),  # x,y
                        self.font,
                        self.font_scale,
                        rank23a_3colors[0],
                        self.line_type)

        # 4段目 10進G値テキスト
        figures = parse_figures(rank23a_color[1])
        for i, figure in enumerate(figures):
            cv2.putText(canvas,
                        f"{figure}",
                        (self.step1_green_bar_rect.left_top[0]+i*2*GRID_INTERVAL_H,
                         top),  # x,y
                        self.font,
                        self.font_scale,
                        rank23a_3colors[1],
                        self.line_type)

        # 4段目 10進B値テキスト
        figures = parse_figures(rank23a_color[2])
        for i, figure in enumerate(figures):
            cv2.putText(canvas,
                        f"{figure}",
                        (self.step1_blue_bar_rect.left_top[0]+i*2*GRID_INTERVAL_H,
                         top),  # x,y
                        self.font,
                        self.font_scale,
                        rank23a_3colors[2],
                        self.line_type)

    def draw_bar_rate_rank13(self, canvas):
        """１段目、３段目のバー率を描きます"""
        rate_y = int((self.top1 + self.top2)/2) - GRID_INTERVAL_H
        cv2.putText(canvas,
                    f"{int(self.rates[0]*100):3}%",
                    (self.right+self.rate_text_gap, rate_y),  # x,y
                    self.font,
                    self.font_scale,
                    LIGHT_GRAY,
                    self.line_type)
        rate_y = int((self.top3 + self.bottom)/2) + GRID_INTERVAL_H
        cv2.putText(canvas,
                    f"{int(self.rates[2]*100):3}%",
                    (self.right+self.rate_text_gap, rate_y),  # x,y
                    self.font,
                    self.font_scale,
                    LIGHT_GRAY,
                    self.line_type)

    def draw_bar_rate_rank2(self, canvas):
        """２段目のバー率を描きます"""
        rate_y = int((self.top2 + self.top3)/2) + GRID_INTERVAL_H
        cv2.putText(canvas,
                    f"{int(self.rates[1]*100):3}%",
                    (self.right+self.rate_text_gap, rate_y),  # x,y
                    self.font,
                    self.font_scale,
                    BLACK,
                    self.line_type)

    def draw_3bars(self, canvas, a_color, step1_color, rank3_color):
        """バーを描きます"""

        # yは逆さ

        # バーR
        cv2.rectangle(canvas, (self.step1_red_bar_rect.left_top[0],
                               self.step1_red_bar_rect.left_top[1]-self.addition_3bars_height[0]),
                      (self.step1_red_bar_rect.right_bottom[0],
                       self.step1_red_bar_rect.left_top[1]), a_color[0], thickness=-1)  # a
        cv2.rectangle(canvas, (self.step1_red_bar_rect.left_top[0],
                               self.step1_red_bar_rect.left_top[1]),
                      self.step1_red_bar_rect.right_bottom, step1_color[0], thickness=-1)  # step1
        cv2.rectangle(canvas, (self.step1_red_bar_rect.left_top[0], self.top3),
                      (self.step1_red_bar_rect.right_bottom[0], self.bottom),
                      rank3_color[0], thickness=-1)  # rank3

        # バーG
        cv2.rectangle(canvas, (self.step1_green_bar_rect.left_top[0],
                               self.step1_green_bar_rect.left_top[1]-self.addition_3bars_height[1]),
                      (self.step1_green_bar_rect.right_bottom[0],
                       self.step1_green_bar_rect.left_top[1]), a_color[1], thickness=-1)
        cv2.rectangle(canvas, (self.step1_green_bar_rect.left_top[0],
                               self.step1_green_bar_rect.left_top[1]),
                      self.step1_green_bar_rect.right_bottom, step1_color[1], thickness=-1)
        cv2.rectangle(canvas, (self.step1_green_bar_rect.left_top[0], self.top3),
                      (self.step1_green_bar_rect.right_bottom[0],
                       self.bottom), rank3_color[1], thickness=-1)

        # バーB
        cv2.rectangle(canvas, (self.step1_blue_bar_rect.left_top[0],
                               self.step1_blue_bar_rect.left_top[1]-self.addition_3bars_height[2]),
                      (self.step1_blue_bar_rect.right_bottom[0],
                       self.step1_blue_bar_rect.left_top[1]), a_color[2], thickness=-1)
        cv2.rectangle(canvas, (self.step1_blue_bar_rect.left_top[0],
                               self.step1_blue_bar_rect.left_top[1]),
                      self.step1_blue_bar_rect.right_bottom, step1_color[2], thickness=-1)
        cv2.rectangle(canvas, (self.step1_blue_bar_rect.left_top[0], self.top3),
                      (self.step1_blue_bar_rect.right_bottom[0],
                       self.bottom), rank3_color[2], thickness=-1)
