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
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
CHANNELS = 3
# モノクロ背景 0黒→255白
MONO_BACKGROUND = 255


def main():
    """一周分の画像を出力
    """

    arc_count = 8
    circumference = 360  # 半径１の円の一周の長さ
    unit_arc = circumference/arc_count  # 等分割した１つの弧

    theta = 0

    # キャンバス
    canvas = np.full((CANVAS_HEIGHT, CANVAS_WIDTH, CHANNELS),
                     MONO_BACKGROUND, dtype=np.uint8)

    center = (200, 200)  # x, y
    box_size = (100, 100)
    # color = RED
    # color = (-255, -255, -255) # 黒
    # color = (-255, 0, 0) # 黒
    color = (255, -255, 0)  # 赤 負値は切り捨て？

    # 円弧
    # 楕円、描画する画像を指定、座標(x,y),xyの半径、角度,色、線の太さ(-1は塗りつぶし)
    cv2.ellipse(canvas,
                center,
                box_size,
                0,
                theta,
                theta+unit_arc,
                color,
                thickness=4)

    # cv2.imshow('Title', canvas)
    # cv2.imwrite('form.jpg',canvas)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # BGRをRGBにする
    canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)

    cv2.imwrite(f"./shared/out-f_step1.png", canvas)


main()
