"""パーサー図。
ただの方眼紙とします"""

import cv2
import numpy as np
from cv2_helper import point_for_cv2, color_for_cv2
from colors import \
    PALE_GRAY, SOFT_GRAY, BLACK
from conf import CANVAS_COLUMNS, CANVAS_ROWS, CANVAS_CHANNELS, GRID_UNIT, TRUE_TYPE_FONT
from japanese import draw_jp


def main():
    """画像を出力します"""

    # キャンバス生成
    canvas = np.full((CANVAS_ROWS*GRID_UNIT, CANVAS_COLUMNS*GRID_UNIT, CANVAS_CHANNELS),
                     color_for_cv2(SOFT_GRAY)[0], dtype=np.uint8)

    # 方眼紙
    # 水平線
    for i in range(0, CANVAS_ROWS+1):
        y_num = GRID_UNIT*i
        cv2.line(canvas,
                 point_for_cv2((0, y_num)),
                 point_for_cv2((CANVAS_COLUMNS*GRID_UNIT, y_num)),
                 color_for_cv2(PALE_GRAY),
                 thickness=1)
    # 垂直線
    for i in range(0, CANVAS_COLUMNS+1):
        x_num = GRID_UNIT*i
        cv2.line(canvas,
                 point_for_cv2((x_num, 0)),
                 point_for_cv2((x_num, CANVAS_ROWS*GRID_UNIT)),
                 color_for_cv2(PALE_GRAY),
                 thickness=1)

    # カンマ区切り テキスト
#    text = """\
#  ,  ,┌ ,─ ,あ,─ ,┐
#  ,  ,├ ,─ ,い,─ ,┤
#  ,  ,├ ,─ ,う,─ ,┤
# ─ ,─ ,┤ ,  ,  ,  ,├ ,─ ,─
#  ,  ,├ ,─ ,え,─ ,┤
#  ,  ,└ ,─ ,お,─ ,┘
# """
    with open('./input/i_step1/screen.csv', encoding='utf8') as f:
        text = f.read()

    # 文字
    for (row, line) in enumerate(text.split('\n')):
        for (column, cell) in enumerate(line.split(',')):
            for (_, char) in enumerate(cell):
                draw_jp(canvas, char, ((column+0.5)*GRID_UNIT, (row+0.5)*GRID_UNIT),
                        TRUE_TYPE_FONT, GRID_UNIT, BLACK)

    # 書出し
    canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)  # BGRをRGBにする
    cv2.imwrite(f"./shared/out-istep1.png", canvas)

    cv2.imshow("make_image.py", canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


main()
