"""パーサー図。
ただの方眼紙とします"""

import cv2
import numpy as np
from cv2_helper import point_for_cv2, color_for_cv2
from colors import \
    PALE_GRAY, BRIGHT_GRAY, SOFT_GRAY, BLACK
from conf import CANVAS_CHANNELS, GRID_UNIT, TRUE_TYPE_FONT
from japanese import draw_jp

FILE_PATH = './@input/i_step2/screen.csv'


def main():
    """画像を出力します"""

    # カンマ区切り テキスト
#    text = """\
#  ,  ,┌ ,─ ,あ,─ ,┐
#  ,  ,├ ,─ ,い,─ ,┤
#  ,  ,├ ,─ ,う,─ ,┤
# ─ ,─ ,┤ ,  ,  ,  ,├ ,─ ,─
#  ,  ,├ ,─ ,え,─ ,┤
#  ,  ,└ ,─ ,お,─ ,┘
# """
    with open(FILE_PATH, encoding='utf8') as file:
        text = file.read()

    # 最大列、最大行を求めます
    lines = text.split('\n')
    max_row = len(lines)
    max_column = 0
    for (row, line) in enumerate(lines):
        cells = len(line.split(','))
        if max_column < cells:
            max_column = cells

    canvas_rows = max_row
    canvas_columns = max_column

    # キャンバス生成
    canvas = np.full((canvas_rows*GRID_UNIT, canvas_columns*GRID_UNIT, CANVAS_CHANNELS),
                     color_for_cv2(PALE_GRAY)[0], dtype=np.uint8)

    # 方眼紙
    # 水平線
    for i in range(0, canvas_rows+1):
        y_num = GRID_UNIT*i
        cv2.line(canvas,
                 point_for_cv2((0, y_num)),
                 point_for_cv2((canvas_columns*GRID_UNIT, y_num)),
                 color_for_cv2(BRIGHT_GRAY),
                 thickness=1)
    # 垂直線
    for i in range(0, canvas_columns+1):
        x_num = GRID_UNIT*i
        cv2.line(canvas,
                 point_for_cv2((x_num, 0)),
                 point_for_cv2((x_num, canvas_rows*GRID_UNIT)),
                 color_for_cv2(BRIGHT_GRAY),
                 thickness=1)

    # 文字
    for (row, line) in enumerate(text.split('\n')):
        for (column, cell) in enumerate(line.split(',')):
            for (_, char) in enumerate(cell):
                draw_jp(canvas, char, ((column+0.5)*GRID_UNIT, (row+0.5)*GRID_UNIT),
                        TRUE_TYPE_FONT, GRID_UNIT, BLACK)

    # 書出し
    canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)  # BGRをRGBにする
    cv2.imwrite(f"./@share/out-istep1.png", canvas)

    cv2.imshow("make_image.py", canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


main()
