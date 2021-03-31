"""正三角形を描きます
一般的に作ってないので、
大きなキャンバスで正常に描けなかったなら、プログラムを見直してください
"""

import math
import cv2
import numpy as np

# 色 BGR
# white = (255, 255, 255)
#PALE_GRAY = (235, 235, 235)
#LIGHT_GRAY = (200, 200, 200)
#BLACK = (16, 16, 16)
#RED = (250, 100, 100)
#GREEN = (100, 250, 100)
#BLUE = (100, 100, 250)

# 描画する画像を作る
# 横幅 約500 以上にすると ブログで縮小されて .gif ではなくなるので、横幅を 約500未満にすること（＾～＾）
#CANVAS_WIDTH = 600
#CANVAS_HEIGHT = 500
#CHANNELS = 3
# モノクロ背景 0黒→255白
#MONO_BACKGROUND = 255


def draw_triangle(canvas, upper_y, lower_y, theta, center, color, thichness):
    """画像を出力
    theta : int
        0時の方向を0°とする時計回りの角度(弧度法)
    """

    # 平行する２本の直線a, b
    # a
    line_a = ((0, upper_y), (10000, upper_y))
    # cv2.line(canvas,
    #         line_a[0],
    #         line_a[1],
    #         PALE_GRAY,
    #         thickness=thichness)
    # b
    line_b = ((0, lower_y), (10000, lower_y))
    # cv2.line(canvas,
    #         line_b[0],
    #         line_b[1],
    #         PALE_GRAY,
    #         thickness=thichness)

    # ある点c
    # cv2.circle(canvas,
    #           center,
    #           5,
    #           PALE_GRAY,
    #           thickness=-1)  # thichness=-1 は塗りつぶし

    # 点cを通るtheta度の直線d
    d_length = 10000
    line_d = make_line(d_length, theta, center)
    # print(
    #    f"line_d=(({line_d[0][0]},{line_d[0][1]}),({line_d[1][0]},{line_d[1][1]}))")
    # d
    # cv2.line(canvas,
    #         line_d[0],
    #         line_d[1],
    #         PALE_GRAY,
    #         thickness=thichness)

    # 線a,dの交点をeとする
    point_e = line_cross(line_a, line_d)
    # cv2.circle(canvas,
    #           point_e,
    #           5,
    #           PALE_GRAY,
    #           thickness=-1)

    # 点e で、線d に対して 30° の２本の直線 f,g が走る
    line_f = make_line(d_length, theta+30, point_e)
    line_g = make_line(d_length, theta-30, point_e)
    # cv2.line(canvas,
    #         line_f[0],
    #         line_f[1],
    #         RED,
    #         thickness=thichness)
    # cv2.line(canvas,
    #         line_g[0],
    #         line_g[1],
    #         GREEN,
    #         thickness=thichness)

    # 線b と、 線 f,g の交点を f', g' とする
    point_fp = line_cross(line_b, line_f)
    point_gp = line_cross(line_b, line_g)
    # cv2.circle(canvas,
    #           point_fp,
    #           5,
    #           RED,
    #           thickness=-1)
    # cv2.circle(canvas,
    #           point_gp,
    #           5,
    #           GREEN,
    #           thickness=-1)

    # 点f', g' のうち、点e に近い方を 点h、
    # 遠い方を 点i とする。
    # 等距離なら どちらでもよい
    distance_fp = distance(point_e, point_fp)
    distance_gp = distance(point_e, point_gp)
    if distance_fp < distance_gp:
        point_h = point_fp
        one_side_len = distance_fp
        next_theta = theta+30+60
    else:
        point_h = point_gp
        one_side_len = distance_gp
        next_theta = theta-30-60

    # cv2.circle(canvas,
    #           point_h,
    #           5,
    #           BLUE,
    #           thickness=-1)
    # cv2.circle(canvas,
    #           point_i,
    #           5,
    #           PALE_GRAY,
    #           thickness=-1)

    # 線分eh, hj のなす角が
    # 60°になるような線分hjを引く。
    # 点jは線分ei上の交点とする
    line_hj = make_beam(one_side_len, next_theta, point_h)
    # cv2.line(canvas,
    #         line_hj[0],
    #         line_hj[1],
    #         RED,
    #         thickness=thichness)

    # 正三角形に必要な３点が求まりました
    triangle_e = point_e
    triangle_h = point_h
    triangle_j = line_hj[1]
    cv2.line(canvas,
             triangle_e,
             triangle_h,
             color,
             thickness=thichness)
    cv2.line(canvas,
             triangle_h,
             triangle_j,
             color,
             thickness=thichness)
    cv2.line(canvas,
             triangle_j,
             triangle_e,
             color,
             thickness=thichness)


def make_line(range1, theta, center):
    """直線((x1,y1),(x2,y2))を求めます"""
    return ((int(range1 * math.sin(math.radians(theta)) + center[0]),
             int(-range1 * math.cos(math.radians(theta)) + center[1])),  # yは逆さ
            (int(range1 * math.sin(math.radians(180+theta)) + center[0]),
             int(-range1 * math.cos(math.radians(180+theta)) + center[1])))


def make_beam(range1, theta, center):
    """直線((x1,y1),(x2,y2))を求めます"""
    return ((center[0], center[1]),  # yは逆さ
            (int(range1 * math.sin(math.radians(theta)) + center[0]),
             int(-range1 * math.cos(math.radians(theta)) + center[1])))


def line_cross(line_ab, line_cd):
    """二直線の交点を求めます。
    https://blog.goo.ne.jp/r-de-r/e/1fa725fab4548e1c0615743dc5ab58b6
    """
    a_x = line_ab[0][0]
    a_y = line_ab[0][1]
    b_x = line_ab[1][0]
    b_y = line_ab[1][1]
    c_x = line_cd[0][0]
    c_y = line_cd[0][1]
    d_x = line_cd[1][0]
    d_y = line_cd[1][1]
    if a_x == b_x and c_x == d_x:
        return (np.nan, np.nan)
    elif a_x == b_x:
        cross_x = a_x
        cross_y = (d_y - c_y) / (d_x - c_x) * (a_x - c_x) + c_y
    elif c_x == d_x:
        cross_x = c_x
        cross_y = (b_y - a_y) / (b_x - a_x) * (c_x - a_x) + a_y
    else:
        work1 = (b_y-a_y)/(b_x-a_x)
        work3 = (d_y-c_y)/(d_x-c_x)
        if work1 == work3:
            return (np.nan, np.nan)
        else:
            cross_x = (work1*a_x-a_y-work3*c_x+c_y)/(work1-work3)
            cross_y = (b_y-a_y)/(b_x-a_x)*(cross_x-a_x)+a_y

    return (int(cross_x), int(cross_y))


def distance(point_a, point_b):
    """２点間の距離を求めます。
    https://tokibito.hatenablog.com/entry/20121222/1356187172
    """
    np_point_a = np.array([point_a[0], point_a[1]])
    np_point_b = np.array([point_b[0], point_b[1]])
    np_diff = np_point_b - np_point_a
    return np.linalg.norm(np_diff)
