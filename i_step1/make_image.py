"""パーサー図。
ただの方眼紙とします"""

import cv2
import numpy as np
from cv2_helper import point_for_cv2, color_for_cv2
from colors import \
    PALE_GRAY, SOFT_GRAY, BLACK
from conf import GRID_UNIT
from japanese import draw_jp

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 800
CHANNELS = 3


def main():
    """画像を出力します"""

    print("Start")

    # キャンバス生成
    canvas = np.full((CANVAS_HEIGHT, CANVAS_WIDTH, CHANNELS),
                     color_for_cv2(SOFT_GRAY)[0], dtype=np.uint8)

    # 方眼紙
    # 水平線
    for i in range(0, int(CANVAS_HEIGHT/GRID_UNIT)+1):
        y_num = GRID_UNIT*i
        cv2.line(canvas,
                 point_for_cv2((0, y_num)),
                 point_for_cv2((CANVAS_WIDTH, y_num)),
                 color_for_cv2(PALE_GRAY),
                 thickness=1)
    # 垂直線
    for i in range(0, int(CANVAS_WIDTH/GRID_UNIT)+1):
        x_num = GRID_UNIT*i
        cv2.line(canvas,
                 point_for_cv2((x_num, 0)),
                 point_for_cv2((x_num, CANVAS_WIDTH)),
                 color_for_cv2(PALE_GRAY),
                 thickness=1)

    # 文字
    draw_jp(canvas, "/", BLACK)

    # 書出し
    canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)  # BGRをRGBにする
    cv2.imwrite(f"./shared/out-istep1.png", canvas)

    cv2.imshow("make_image.py", canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


main()
