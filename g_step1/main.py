"""png画像を複数枚出力します
"""

import math
import cv2
import numpy as np

# 色 BGR
# white = (255, 255, 255)
PALE_GRAY = (235, 235, 235)
LIGHT_GRAY = (200, 200, 200)
BLACK = (16, 16, 16)
RED = (250, 100, 100)
GREEN = (100, 250, 100)
BLUE = (100, 100, 250)

# 描画する画像を作る
# 横幅 約500 以上にすると ブログで縮小されて .gif ではなくなるので、横幅を 約500未満にすること（＾～＾）
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 500
CHANNELS = 3
# モノクロ背景 0黒→255白
MONO_BACKGROUND = 255


def main():
    """画像を出力
    """

    # キャンバス
    canvas = np.full((CANVAS_HEIGHT, CANVAS_WIDTH, CHANNELS),
                     MONO_BACKGROUND, dtype=np.uint8)

    thichness = 2

    # 平行する２本の直線a, b
    # a
    line_a = ((10, 100), (400, 100))
    cv2.line(canvas,
             line_a[0],
             line_a[1],
             PALE_GRAY,
             thickness=thichness)
    # b
    line_b = ((10, 300), (400, 300))
    cv2.line(canvas,
             line_b[0],
             line_b[1],
             PALE_GRAY,
             thickness=thichness)

    # ある点c
    point_c = (280, 220)
    cv2.circle(canvas,
               point_c,
               5,
               PALE_GRAY,
               thickness=-1)  # thichness=-1 は塗りつぶし

    # 0時の方向を0°とする時計回りの角度(弧度法)
    theta = 25

    # 点cを通るtheta度の直線d
    d_length = 800
    line_d = make_line(d_length, theta, point_c)
    print(
        f"line_d=(({line_d[0][0]},{line_d[0][1]}),({line_d[1][0]},{line_d[1][1]}))")
    # d
    cv2.line(canvas,
             line_d[0],
             line_d[1],
             PALE_GRAY,
             thickness=thichness)

    # 線a,dの交点をeとする
    point_e = line_cross(line_a, line_d)
    cv2.circle(canvas,
               point_e,
               5,
               PALE_GRAY,
               thickness=-1)

    # 点e で、線d に対して 30° の２本の直線 f,g が走る
    line_f = make_line(d_length, theta+30, point_e)
    line_g = make_line(d_length, theta-30, point_e)
    cv2.line(canvas,
             line_f[0],
             line_f[1],
             RED,
             thickness=thichness)
    cv2.line(canvas,
             line_g[0],
             line_g[1],
             GREEN,
             thickness=thichness)

    # 線b と、 線 f,g の交点を f', g' とする
    point_fp = line_cross(line_b, line_f)
    point_gp = line_cross(line_b, line_g)
    cv2.circle(canvas,
               point_fp,
               5,
               RED,
               thickness=-1)
    cv2.circle(canvas,
               point_gp,
               5,
               GREEN,
               thickness=-1)

    # cv2.imshow('Title', canvas)
    # cv2.imwrite('form.jpg',canvas)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # BGRをRGBにする
    canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)

    cv2.imwrite(f"./shared/out-g_step1.png", canvas)


def make_line(range1, theta, center):
    """直線((x1,y1),(x2,y2))を求めます"""
    return ((int(range1 * math.sin(math.radians(theta)) + center[0]),
             int(-range1 * math.cos(math.radians(theta)) + center[1])),  # yは逆さ
            (int(range1 * math.sin(math.radians(180+theta)) + center[0]),
             int(-range1 * math.cos(math.radians(180+theta)) + center[1])))


def line_cross(line_ab, line_cd):
    """二直線の交点を求める。
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


main()
