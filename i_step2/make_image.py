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
LINE_THICKNESS = 2
FONT_THICKNESS = 1
GRID_COLOR = BRIGHT_GRAY
LINE_COLOR = SOFT_GRAY
FONT_COLOR = BLACK


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
                 color_for_cv2(GRID_COLOR),
                 thickness=1)
    # 垂直線
    for i in range(0, canvas_columns+1):
        x_num = GRID_UNIT*i
        cv2.line(canvas,
                 point_for_cv2((x_num, 0)),
                 point_for_cv2((x_num, canvas_rows*GRID_UNIT)),
                 color_for_cv2(GRID_COLOR),
                 thickness=1)

    # 文字 または 図形
    for (row, line) in enumerate(text.split('\n')):
        for (column, cell) in enumerate(line.split(',')):

            if cell.strip() == '..':
                # '..' 半角スペース
                draw_space(canvas, column, row)
                continue

            for (_, char) in enumerate(cell):
                if char == '↑':
                    draw_up_arrow(canvas, column, row)
                elif char == '→':
                    draw_right_arrow(canvas, column, row)
                elif char == '↓':
                    draw_down_arrow(canvas, column, row)
                elif char == '←':
                    draw_left_arrow(canvas, column, row)
                elif char == '─':
                    draw_horizontal_line(canvas, column, row)
                elif char == '│':
                    draw_vertical_line(canvas, column, row)
                elif char == '┌':
                    draw_left_top_corner(canvas, column, row)
                elif char == '┐':
                    draw_right_top_corner(canvas, column, row)
                elif char == '┘':
                    draw_right_bottom_corner(canvas, column, row)
                elif char == '└':
                    draw_left_bottom_corner(canvas, column, row)
                elif char == '┴':
                    draw_up_tee(canvas, column, row)
                elif char == '├':
                    draw_right_tee(canvas, column, row)
                elif char == '┬':
                    draw_down_tee(canvas, column, row)
                elif char == '┤':
                    draw_left_tee(canvas, column, row)
                else:
                    draw_jp(canvas, char, ((column+0.5)*GRID_UNIT, (row+0.5)*GRID_UNIT),
                            TRUE_TYPE_FONT, GRID_UNIT, FONT_COLOR)

    # 書出し
    canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)  # BGRをRGBにする
    cv2.imwrite(f"./@share/out-istep1.png", canvas)

    cv2.imshow("make_image.py", canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def draw_horizontal_line(canvas, column, row):
    """─描画"""
    left = column*GRID_UNIT
    right = (column+1)*GRID_UNIT
    top = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((right, top)),
             color_for_cv2(LINE_COLOR),
             thickness=LINE_THICKNESS)


def draw_vertical_line(canvas, column, row):
    """│描画"""
    left = (column+0.5)*GRID_UNIT
    top = row*GRID_UNIT
    bottom = (row+1)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((left, bottom)),
             color_for_cv2(LINE_COLOR),
             thickness=LINE_THICKNESS)


def draw_left_top_corner(canvas, column, row):
    """┌描画"""
    # 水平線部
    left = (column+0.5)*GRID_UNIT
    right = (column+1)*GRID_UNIT
    top = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((right, top)),
             color_for_cv2(LINE_COLOR),
             thickness=LINE_THICKNESS)
    # 垂直線部
    left = (column+0.5)*GRID_UNIT
    top = (row+0.5)*GRID_UNIT
    bottom = (row+1)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((left, bottom)),
             color_for_cv2(LINE_COLOR),
             thickness=LINE_THICKNESS)


def draw_right_top_corner(canvas, column, row):
    """┐描画"""
    # 水平線部
    left = (column+0)*GRID_UNIT
    right = (column+0.5)*GRID_UNIT
    top = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((right, top)),
             color_for_cv2(LINE_COLOR),
             thickness=LINE_THICKNESS)
    # 垂直線部
    left = (column+0.5)*GRID_UNIT
    top = (row+0.5)*GRID_UNIT
    bottom = (row+1)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((left, bottom)),
             color_for_cv2(LINE_COLOR),
             thickness=LINE_THICKNESS)


def draw_right_bottom_corner(canvas, column, row):
    """┘描画"""
    # 水平線部
    left = (column+0)*GRID_UNIT
    right = (column+0.5)*GRID_UNIT
    top = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((right, top)),
             color_for_cv2(LINE_COLOR),
             thickness=LINE_THICKNESS)
    # 垂直線部
    left = (column+0.5)*GRID_UNIT
    top = (row+0)*GRID_UNIT
    bottom = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((left, bottom)),
             color_for_cv2(LINE_COLOR),
             thickness=LINE_THICKNESS)


def draw_left_bottom_corner(canvas, column, row):
    """└描画"""
    # 水平線部
    left = (column+0.5)*GRID_UNIT
    right = (column+1)*GRID_UNIT
    top = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((right, top)),
             color_for_cv2(LINE_COLOR),
             thickness=LINE_THICKNESS)
    # 垂直線部
    left = (column+0.5)*GRID_UNIT
    top = (row+0)*GRID_UNIT
    bottom = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((left, bottom)),
             color_for_cv2(LINE_COLOR),
             thickness=LINE_THICKNESS)


def draw_up_tee(canvas, column, row):
    """┴描画"""
    # 水平線部
    left = (column+0)*GRID_UNIT
    right = (column+1)*GRID_UNIT
    top = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((right, top)),
             color_for_cv2(LINE_COLOR),
             thickness=LINE_THICKNESS)
    # 垂直線部
    left = (column+0.5)*GRID_UNIT
    top = (row+0)*GRID_UNIT
    bottom = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((left, bottom)),
             color_for_cv2(LINE_COLOR),
             thickness=LINE_THICKNESS)


def draw_right_tee(canvas, column, row):
    """├描画"""
    # 水平線部
    left = (column+0.5)*GRID_UNIT
    right = (column+1)*GRID_UNIT
    top = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((right, top)),
             color_for_cv2(LINE_COLOR),
             thickness=LINE_THICKNESS)
    # 垂直線部
    left = (column+0.5)*GRID_UNIT
    top = (row+0)*GRID_UNIT
    bottom = (row+1)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((left, bottom)),
             color_for_cv2(LINE_COLOR),
             thickness=LINE_THICKNESS)


def draw_down_tee(canvas, column, row):
    """┬描画"""
    # 水平線部
    left = (column+0)*GRID_UNIT
    right = (column+1)*GRID_UNIT
    top = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((right, top)),
             color_for_cv2(LINE_COLOR),
             thickness=LINE_THICKNESS)
    # 垂直線部
    left = (column+0.5)*GRID_UNIT
    top = (row+0.5)*GRID_UNIT
    bottom = (row+1)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((left, bottom)),
             color_for_cv2(LINE_COLOR),
             thickness=LINE_THICKNESS)


def draw_left_tee(canvas, column, row):
    """┤描画"""
    # 水平線部
    left = (column+0)*GRID_UNIT
    right = (column+0.5)*GRID_UNIT
    top = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((right, top)),
             color_for_cv2(LINE_COLOR),
             thickness=LINE_THICKNESS)
    # 垂直線部
    left = (column+0.5)*GRID_UNIT
    top = (row+0)*GRID_UNIT
    bottom = (row+1)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((left, bottom)),
             color_for_cv2(LINE_COLOR),
             thickness=LINE_THICKNESS)


def draw_space(canvas, column, row):
    """半角スペースを三角形で描画"""
    center = (column+0.5)*GRID_UNIT
    bottom2 = (row+0.8)*GRID_UNIT
    # 底辺部
    left = (column+0.1)*GRID_UNIT
    right = (column+0.9)*GRID_UNIT
    bottom = (row+1)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, bottom)),
             point_for_cv2((right, bottom)),
             color_for_cv2(FONT_COLOR),
             thickness=FONT_THICKNESS)
    # 左斜辺
    left2 = (column+0.1)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left2, bottom)),
             point_for_cv2((center, bottom2)),
             color_for_cv2(FONT_COLOR),
             thickness=FONT_THICKNESS)
    # 右斜辺
    left2 = (column+0.9)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((center, bottom2)),
             point_for_cv2((right, bottom)),
             color_for_cv2(FONT_COLOR),
             thickness=FONT_THICKNESS)


def draw_up_arrow(canvas, column, row):
    """↑描画"""
    left = (column+0.5)*GRID_UNIT
    top = (row+0.2)*GRID_UNIT
    bottom = (row+1)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((left, bottom)),
             color_for_cv2(LINE_COLOR),
             thickness=LINE_THICKNESS)
    # 矢頭
    left2 = (column+0.2)*GRID_UNIT
    top2 = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((left2, top2)),
             color_for_cv2(LINE_COLOR),
             thickness=LINE_THICKNESS)
    # 矢頭
    left2 = (column+0.8)*GRID_UNIT
    top2 = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((left2, top2)),
             color_for_cv2(LINE_COLOR),
             thickness=LINE_THICKNESS)


def draw_right_arrow(canvas, column, row):
    """→描画"""
    left = column*GRID_UNIT
    right = (column+0.8)*GRID_UNIT
    top = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((right, top)),
             color_for_cv2(LINE_COLOR),
             thickness=LINE_THICKNESS)
    # 矢頭
    right2 = (column+0.5)*GRID_UNIT
    top2 = (row+0.2)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((right, top)),
             point_for_cv2((right2, top2)),
             color_for_cv2(LINE_COLOR),
             thickness=LINE_THICKNESS)
    # 矢頭
    right2 = (column+0.5)*GRID_UNIT
    top2 = (row+0.8)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((right, top)),
             point_for_cv2((right2, top2)),
             color_for_cv2(LINE_COLOR),
             thickness=LINE_THICKNESS)


def draw_down_arrow(canvas, column, row):
    """↓描画"""
    left = (column+0.5)*GRID_UNIT
    top = row*GRID_UNIT
    bottom = (row+0.8)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((left, bottom)),
             color_for_cv2(LINE_COLOR),
             thickness=LINE_THICKNESS)
    # 矢頭
    left2 = (column+0.2)*GRID_UNIT
    bottom2 = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, bottom)),
             point_for_cv2((left2, bottom2)),
             color_for_cv2(LINE_COLOR),
             thickness=LINE_THICKNESS)
    # 矢頭
    left2 = (column+0.8)*GRID_UNIT
    bottom2 = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, bottom)),
             point_for_cv2((left2, bottom2)),
             color_for_cv2(LINE_COLOR),
             thickness=LINE_THICKNESS)


def draw_left_arrow(canvas, column, row):
    """←描画"""
    left = (column+0.2)*GRID_UNIT
    right = (column+1)*GRID_UNIT
    top = (row+0.5)*GRID_UNIT
    # 線
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((right, top)),
             color_for_cv2(LINE_COLOR),
             thickness=LINE_THICKNESS)
    # 矢頭
    left2 = (column+0.5)*GRID_UNIT
    top2 = (row+0.2)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((left2, top2)),
             color_for_cv2(LINE_COLOR),
             thickness=LINE_THICKNESS)
    # 矢頭
    left2 = (column+0.5)*GRID_UNIT
    top2 = (row+0.8)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((left2, top2)),
             color_for_cv2(LINE_COLOR),
             thickness=LINE_THICKNESS)


main()
