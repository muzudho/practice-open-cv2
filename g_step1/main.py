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
CANVAS_WIDTH = 500
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
    cv2.line(canvas,
             (10, 100),
             (400, 100),
             PALE_GRAY,
             thickness=thichness)
    # b
    cv2.line(canvas,
             (10, 300),
             (400, 300),
             PALE_GRAY,
             thickness=thichness)

    # ある点c
    point_c = (200, 200)
    cv2.circle(canvas,
               point_c,
               5,
               PALE_GRAY,
               thickness=-1)  # thichness=-1 は塗りつぶし

    # 0時の方向を0°とする時計回りの角度(弧度法)
    theta = 25

    # 点cを通るtheta度の直線d
    d_length = 300
    d_p1 = (int(d_length * math.sin(math.radians(theta)) + point_c[0]),
            int(d_length * -math.sin(math.radians(theta)) + point_c[0]))  # yは逆さ
    d_p2 = (int(d_length * math.sin(math.radians(360-theta)) + point_c[0]),
            int(d_length * -math.sin(math.radians(360-theta)) + point_c[0]))
    # d
    cv2.line(canvas,
             d_p1,
             d_p2,
             PALE_GRAY,
             thickness=thichness)

    # cv2.imshow('Title', canvas)
    # cv2.imwrite('form.jpg',canvas)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # BGRをRGBにする
    canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)

    cv2.imwrite(f"./shared/out-g_step1.png", canvas)


main()
