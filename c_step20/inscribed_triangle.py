"""内接する正三角形
"""

import cv2
from triangle import calc_triangle
from colors import RED, GREEN, BLUE, BLACK
from conf import GRID_UNIT


class InscribedTriangle():
    """内接する正三角形"""

    def __init__(self):
        self.__rbg_points = ((0, 0), (0, 0), (0, 0))

    @property
    def rbg_points(self):
        """円周上の点R,B,G"""
        return self.__rbg_points

    def triangular_center_of_gravity(self):
        """三角形の重心"""
        return (
            int((self.__rbg_points[0][0]+self.__rbg_points[1]
                 [0]+self.__rbg_points[2][0])/3),
            int((self.__rbg_points[0][1]+self.__rbg_points[1][1]+self.__rbg_points[2][1])/3))

    def correct_horizon(self, diff_xy):
        """水平方向のずれの修正"""
        self.__rbg_points = (
            (self.__rbg_points[0][0] - diff_xy[0],
             self.__rbg_points[0][1]),
            (self.__rbg_points[1][0] - diff_xy[0],
             self.__rbg_points[1][1]),
            (self.__rbg_points[2][0] - diff_xy[0],
             self.__rbg_points[2][1])
        )

    def update(self, top2, top3, center, theta, rank23d_3bars_height):
        """円に内接する線。正三角形"""

        # 赤、緑、青 の点の位置関係は全部で１２相です
        red = rank23d_3bars_height[0]
        green = rank23d_3bars_height[1]
        blue = rank23d_3bars_height[2]
        triangle_theta = theta  # +phase*30
        if green == blue and blue < red:
            # 緑と青は等しく、それより赤が上
            phase = 0  # トライアングル・フェーズ
        elif blue < green and green < red:
            # 下から青、緑、赤
            phase = 1
        elif blue < green and green == red:
            # 青より大きい緑は赤と等しい
            phase = 2
        elif blue < red and red < green:
            # 下から青、赤、緑
            phase = 3
            triangle_theta -= 120
        elif blue == red and red < green:
            # 青と赤は等しく、それより緑が上
            phase = 4
            triangle_theta -= 120
        elif red < blue and blue < green:
            # 下から赤、青、緑
            phase = 5
            triangle_theta -= 120
        elif red < blue and blue == green:
            # 赤より大きい青は緑と等しい
            phase = 6
            triangle_theta -= 120
        elif red < green and green < blue:
            # 下から赤、緑、青
            phase = 7
            triangle_theta += 120
        elif red == green and green < blue:
            # 赤と緑は等しく、それより青が上
            phase = 8
            triangle_theta += 120
        elif green < red and red < blue:
            # 下から緑、赤、青
            phase = 9
            triangle_theta += 120
        elif green < red and red == blue:
            # 緑より大きい赤は青と等しい
            phase = 10
        else:
            # 下から緑、青、赤
            phase = 11
        # 赤、青、緑 の順なのが工夫
        self.__rbg_points = calc_triangle(top2,
                                          top3,
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
            self.__rbg_points = (
                self.rbg_points[2], self.rbg_points[1], self.rbg_points[0])
        elif phase == 4:
            # 青や赤より緑が上
            self.__rbg_points = (
                self.rbg_points[1], self.rbg_points[2], self.rbg_points[0])
        elif phase == 5:
            # 下から赤、青、緑
            self.__rbg_points = (
                self.rbg_points[1], self.rbg_points[2], self.rbg_points[0])
        elif phase == 6:
            # 赤より、青と緑が上
            self.__rbg_points = (
                self.rbg_points[1], self.rbg_points[2], self.rbg_points[0])
        elif phase == 7:
            # 下から赤、緑、青
            self.__rbg_points = (
                self.rbg_points[1], self.rbg_points[0], self.rbg_points[2])
        elif phase == 8:
            # 赤や緑より青が上
            self.__rbg_points = (
                self.rbg_points[2], self.rbg_points[0], self.rbg_points[1])
        elif phase == 9:
            # 下から緑、赤、青
            self.__rbg_points = (
                self.rbg_points[2], self.rbg_points[0], self.rbg_points[1])
        elif phase == 10:
            # 緑より、赤と青が上
            self.__rbg_points = (
                self.rbg_points[0], self.rbg_points[2], self.rbg_points[1])
        else:
            # 下から緑、青、赤
            self.__rbg_points = (
                self.rbg_points[0], self.rbg_points[2], self.rbg_points[1])

    def draw(self, canvas):
        """描きます"""
        cv2.line(canvas,
                 self.rbg_points[0],
                 self.rbg_points[1],
                 BLACK,
                 thickness=2)
        cv2.line(canvas,
                 self.rbg_points[1],
                 self.rbg_points[2],
                 BLACK,
                 thickness=2)
        cv2.line(canvas,
                 self.rbg_points[2],
                 self.rbg_points[0],
                 BLACK,
                 thickness=2)
        cv2.circle(canvas, self.rbg_points[0],
                   int(GRID_UNIT/4), RED, thickness=-1)
        cv2.circle(canvas, self.rbg_points[1],
                   int(GRID_UNIT/4), BLUE, thickness=-1)
        cv2.circle(canvas, self.rbg_points[2],
                   int(GRID_UNIT/4), GREEN, thickness=-1)
