"""内接する正三角形
"""

import math
import cv2
from triangle_calc import calc_triangle
from colors import GRAY
from conf import BAR_TICKS
from cv2_helper import point_for_cv2, color_for_cv2
from color_hul_model import color_phase


class Triangle():
    """内接する正三角形"""

    def __init__(self):
        self.__edge_color = GRAY
        self.__nodes_p = ((0, 0), (0, 0), (0, 0))
        self.__nodes_color = (GRAY, GRAY, GRAY)
        self.__node_radius = 0
        self.__center_color = GRAY

    @property
    def edge_color(self):
        """辺の色"""
        return self.__edge_color

    @edge_color.setter
    def edge_color(self, val):
        self.__edge_color = val

    @property
    def nodes_p(self):
        """円周上の点R,B,G"""
        return self.__nodes_p

    @nodes_p.setter
    def nodes_p(self, val):
        self.__nodes_p = val

    @property
    def nodes_color(self):
        """頂点の色"""
        return self.__nodes_color

    @nodes_color.setter
    def nodes_color(self, val):
        self.__nodes_color = val

    @property
    def node_radius(self):
        """円周上の点の半径"""
        return self.__node_radius

    @node_radius.setter
    def node_radius(self, val):
        self.__node_radius = val

    @property
    def center_color(self):
        """重心の色"""
        return self.__center_color

    @center_color.setter
    def center_color(self, val):
        self.__center_color = val

    def triangular_center_of_gravity(self):
        """三角形の重心"""
        return (
            (self.__nodes_p[0][0]+self.__nodes_p[1]
             [0]+self.__nodes_p[2][0])/3,
            (self.__nodes_p[0][1]+self.__nodes_p[1][1]+self.__nodes_p[2][1])/3)

    def correct_horizon(self, diff_xy):
        """垂直方向のずれの修正"""
        # 水平方向には ずれてください
        self.__nodes_p = (
            (self.__nodes_p[0][0],
             self.__nodes_p[0][1] - diff_xy[1]),
            (self.__nodes_p[1][0],
             self.__nodes_p[1][1] - diff_xy[1]),
            (self.__nodes_p[2][0],
             self.__nodes_p[2][1] - diff_xy[1])
        )

    def update(self, upper_x, lower_x, center, theta, n3bars_len, bar_box_width):
        """円に内接する線。正三角形"""

        color = (n3bars_len[0]/bar_box_width,
                 n3bars_len[1]/bar_box_width,
                 n3bars_len[2]/bar_box_width)
        c_phase = color_phase(color)

        # 赤、緑、青 の点の位置関係は全部で１２相です
        red = n3bars_len[0]
        green = n3bars_len[1]
        blue = n3bars_len[2]
        triangle_theta = theta
        if c_phase == 'A1':  # green == blue and blue < red:
            # 緑と青は等しく、それより赤が大きい
            phase = 0  # トライアングル・フェーズ
        elif blue < green < red:
            # 下から青、緑、赤
            phase = 1
        elif c_phase == 'A2':  # blue < green and green == red:
            # 赤と緑は等しく、それより青は小さい
            phase = 2
        elif blue < red < green:
            # 下から青、赤、緑
            phase = 3
            triangle_theta -= math.radians(120)
        elif c_phase == 'A3':  # blue == red and red < green:
            # 青と赤は等しく、それより緑が大きい
            phase = 4
            triangle_theta -= math.radians(120)
        elif red < blue < green:
            # 下から赤、青、緑
            phase = 5
            triangle_theta -= math.radians(120)
        elif c_phase == 'A4':  # red < blue and blue == green:
            # 緑と青は等しく、それより赤は小さい
            phase = 6
            triangle_theta -= math.radians(120)
        elif red < green < blue:
            # 下から赤、緑、青
            phase = 7
            triangle_theta += math.radians(120)
        elif c_phase == 'A5':  # red == green and green < blue:
            # 赤と緑は等しく、それより青が大きい
            phase = 8
            triangle_theta += math.radians(120)
        elif green < red < blue:
            # 下から緑、赤、青
            phase = 9
            triangle_theta += math.radians(120)
        elif c_phase == 'A6':  # green < red and red == blue:
            # 赤と青は等しく、それより緑が小さい
            phase = 10
        else:
            # 下から緑、青、赤
            phase = 11
        # 赤、青、緑 の順なのが工夫
        self.__nodes_p = calc_triangle(upper_x,
                                       lower_x,
                                       triangle_theta,
                                       center)
        if phase == 0:
            # 緑や青より赤が上
            pass
        elif phase == 1:
            # 下から青、緑、赤
            pass
        elif phase == 2:
            # 青より、緑と赤が上
            pass
        elif phase == 3:
            # 下から青、赤、緑
            self.__nodes_p = (
                self.nodes_p[2], self.nodes_p[1], self.nodes_p[0])
        elif phase == 4:
            # 青や赤より緑が上
            self.__nodes_p = (
                self.nodes_p[1], self.nodes_p[2], self.nodes_p[0])
        elif phase == 5:
            # 下から赤、青、緑
            self.__nodes_p = (
                self.nodes_p[1], self.nodes_p[2], self.nodes_p[0])
        elif phase == 6:
            # 赤より、青と緑が上
            self.__nodes_p = (
                self.nodes_p[1], self.nodes_p[2], self.nodes_p[0])
        elif phase == 7:
            # 下から赤、緑、青
            self.__nodes_p = (
                self.nodes_p[1], self.nodes_p[0], self.nodes_p[2])
        elif phase == 8:
            # 赤や緑より青が上
            self.__nodes_p = (
                self.nodes_p[2], self.nodes_p[0], self.nodes_p[1])
        elif phase == 9:
            # 下から緑、赤、青
            self.__nodes_p = (
                self.nodes_p[2], self.nodes_p[0], self.nodes_p[1])
        elif phase == 10:
            # 緑より、赤と青が上
            self.__nodes_p = (
                self.nodes_p[0], self.nodes_p[2], self.nodes_p[1])
        else:
            # 下から緑、青、赤
            self.__nodes_p = (
                self.nodes_p[0], self.nodes_p[2], self.nodes_p[1])

    def draw(self, canvas):
        """描きます"""
        # ３辺
        cv2.line(canvas,
                 point_for_cv2(self.nodes_p[0]),
                 point_for_cv2(self.nodes_p[1]),
                 color_for_cv2(self.__edge_color, BAR_TICKS),
                 thickness=2)
        cv2.line(canvas,
                 point_for_cv2(self.nodes_p[1]),
                 point_for_cv2(self.nodes_p[2]),
                 color_for_cv2(self.__edge_color, BAR_TICKS),
                 thickness=2)
        cv2.line(canvas,
                 point_for_cv2(self.nodes_p[2]),
                 point_for_cv2(self.nodes_p[0]),
                 color_for_cv2(self.__edge_color, BAR_TICKS),
                 thickness=2)
        # ３頂点
        if self.__node_radius > 0:
            cv2.circle(canvas,
                       point_for_cv2(self.nodes_p[0]),
                       int(self.__node_radius),
                       color_for_cv2(self.__nodes_color[0], BAR_TICKS),
                       thickness=-1)
            cv2.circle(canvas,
                       point_for_cv2(self.nodes_p[1]),
                       int(self.__node_radius),
                       color_for_cv2(self.__nodes_color[2], BAR_TICKS),
                       thickness=-1)
            cv2.circle(canvas,
                       point_for_cv2(self.nodes_p[2]),
                       int(self.__node_radius),
                       color_for_cv2(self.__nodes_color[1], BAR_TICKS),
                       thickness=-1)

            # 重心
            gravity = self.triangular_center_of_gravity()
            cv2.circle(canvas,
                       point_for_cv2(gravity),
                       int(self.__node_radius),
                       color_for_cv2(self.__center_color, BAR_TICKS),
                       thickness=-1)
