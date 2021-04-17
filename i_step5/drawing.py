"""描画"""

import cv2
from cv2_helper import point_for_cv2, color_for_cv2
from japanese import draw_jp
from conf import GRID_UNIT, TRUE_TYPE_FONT, LINE_THICKNESS, FONT_THICKNESS
from conf2 import GRID_COLOR, LINE_COLOR, FONT_COLOR, START_COLOR, GOAL_COLOR, AGENT_COLOR, \
    CHECKED_FORWARD_COLOR, CHECKED_BACKWARD_COLOR


def draw_board(canvas, board):
    """盤の描画"""

    # 方眼紙
    # 水平線
    for i in range(0, board.height+1):
        y_num = GRID_UNIT*i
        cv2.line(canvas,
                 point_for_cv2((0, y_num)),
                 point_for_cv2((board.width*GRID_UNIT, y_num)),
                 color_for_cv2(GRID_COLOR),
                 thickness=1)
    # 垂直線
    for i in range(0, board.width+1):
        x_num = GRID_UNIT*i
        cv2.line(canvas,
                 point_for_cv2((x_num, 0)),
                 point_for_cv2((x_num, board.height*GRID_UNIT)),
                 color_for_cv2(GRID_COLOR),
                 thickness=1)

    # 文字 または 図形
    for (row, columns) in enumerate(board.rows):
        for (column, cell) in enumerate(columns):

            # チェック済みマーク
            if board.checked_table[row][column] == 'f':
                font_color = line_color = CHECKED_FORWARD_COLOR
            elif board.checked_table[row][column] == 'b':
                font_color = line_color = CHECKED_BACKWARD_COLOR
            else:
                line_color = LINE_COLOR
                font_color = FONT_COLOR

            cell = cell.strip()
            ligature = False
            # Ligature(合字;リガチャ)
            if cell == '..':
                # '..' 半角スペース
                draw_space(canvas, column, row, font_color)
                ligature = True
            elif cell == 'Start':
                draw_circle(canvas, column, row, START_COLOR)
                draw_jp(canvas, 'S', ((column+0.5)*GRID_UNIT, (row+0.5)*GRID_UNIT),
                        TRUE_TYPE_FONT, GRID_UNIT, FONT_COLOR)
                board.start_location = (column, row)
                ligature = True
            elif cell == 'Goal':
                draw_circle(canvas, column, row, GOAL_COLOR)
                draw_jp(canvas, 'G', ((column+0.5)*GRID_UNIT, (row+0.5)*GRID_UNIT),
                        TRUE_TYPE_FONT, GRID_UNIT, FONT_COLOR)
                ligature = True
            elif cell == '┌r':
                draw_left_top_round_corner(canvas, column, row, line_color)
                ligature = True
            elif cell == '┐r':
                draw_right_top_round_corner(canvas, column, row, line_color)
                ligature = True
            elif cell == '┘r':
                draw_right_bottom_round_corner(canvas, column, row, line_color)
                ligature = True
            elif cell == '└r':
                draw_left_bottom_round_corner(canvas, column, row, line_color)
                ligature = True
            elif cell == '└r':
                draw_left_bottom_round_corner(canvas, column, row, line_color)
                ligature = True
            elif cell == '┘└':
                draw_left_bottom_round_corner(canvas, column, row, line_color)
                draw_right_bottom_round_corner(canvas, column, row, line_color)
                ligature = True
            elif cell in ('└┌', '┌└'):
                draw_left_bottom_round_corner(canvas, column, row, line_color)
                draw_left_top_round_corner(canvas, column, row, line_color)
                ligature = True
            elif cell == '┐┌':
                draw_right_top_round_corner(canvas, column, row, line_color)
                draw_left_top_round_corner(canvas, column, row, line_color)
                ligature = True
            elif cell in ('┘┐', '┐┘'):
                draw_right_bottom_round_corner(canvas, column, row, line_color)
                draw_right_top_round_corner(canvas, column, row, line_color)
                ligature = True
            elif cell == '│┌':
                draw_vertical_line(canvas, column, row, line_color)
                draw_left_top_round_corner(canvas, column, row, line_color)
                ligature = True
            elif cell == '┐│':
                draw_vertical_line(canvas, column, row, line_color)
                draw_right_top_round_corner(canvas, column, row, line_color)
                ligature = True
            elif cell == '┘│':
                draw_vertical_line(canvas, column, row, line_color)
                draw_right_bottom_round_corner(canvas, column, row, line_color)
                ligature = True
            elif cell == '│└':
                draw_vertical_line(canvas, column, row, line_color)
                draw_left_bottom_round_corner(canvas, column, row, line_color)
                ligature = True
            elif cell == '─┌':
                draw_horizontal_line(canvas, column, row, line_color)
                draw_left_top_round_corner(canvas, column, row, line_color)
                ligature = True
            elif cell == '─┌':
                draw_horizontal_line(canvas, column, row, line_color)
                draw_right_top_round_corner(canvas, column, row, line_color)
                ligature = True
            elif cell == '┘─':
                draw_horizontal_line(canvas, column, row, line_color)
                draw_right_bottom_round_corner(canvas, column, row, line_color)
                ligature = True
            elif cell == '─└':
                draw_horizontal_line(canvas, column, row, line_color)
                draw_left_bottom_round_corner(canvas, column, row, line_color)
                ligature = True

            if not ligature:
                for (_, char) in enumerate(cell):
                    if char == '↑':
                        draw_up_arrow(canvas, column, row, line_color)
                    elif char == '→':
                        draw_right_arrow(canvas, column, row, line_color)
                    elif char == '↓':
                        draw_down_arrow(canvas, column, row, line_color)
                    elif char == '←':
                        draw_left_arrow(canvas, column, row, line_color)
                    elif char == '─':
                        draw_horizontal_line(canvas, column, row, line_color)
                    elif char == '│':
                        draw_vertical_line(canvas, column, row, line_color)
                    elif char == '┌':
                        draw_left_top_corner(canvas, column, row, line_color)
                    elif char == '┐':
                        draw_right_top_corner(canvas, column, row, line_color)
                    elif char == '┘':
                        draw_right_bottom_corner(
                            canvas, column, row, line_color)
                    elif char == '└':
                        draw_left_bottom_corner(
                            canvas, column, row, line_color)
                    elif char == '┴':
                        draw_up_tee(canvas, column, row, line_color)
                    elif char == '├':
                        draw_right_tee(canvas, column, row, line_color)
                    elif char == '┬':
                        draw_down_tee(canvas, column, row, line_color)
                    elif char == '┤':
                        draw_left_tee(canvas, column, row, line_color)
                    else:
                        draw_jp(canvas, char, ((column+0.5)*GRID_UNIT, (row+0.5)*GRID_UNIT),
                                TRUE_TYPE_FONT, GRID_UNIT, font_color)

            # チェック済みマーク
            # if board.checked_table[row][column] == 'f':
            #    draw_cross(canvas, column, row, CHECKED_FORWARD_COLOR)
            # elif board.checked_table[row][column] == 'b':
            #    draw_cross(canvas, column, row, CHECKED_BACKWARD_COLOR)


def draw_horizontal_line(canvas, column, row, line_color):
    """─描画"""
    left = column*GRID_UNIT
    right = (column+1)*GRID_UNIT
    top = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((right, top)),
             color_for_cv2(line_color),
             thickness=LINE_THICKNESS)


def draw_vertical_line(canvas, column, row, line_color):
    """│描画"""
    left = (column+0.5)*GRID_UNIT
    top = row*GRID_UNIT
    bottom = (row+1)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((left, bottom)),
             color_for_cv2(line_color),
             thickness=LINE_THICKNESS)


def draw_left_top_corner(canvas, column, row, line_color):
    """┌描画"""
    # 水平線部
    left = (column+0.5)*GRID_UNIT
    right = (column+1)*GRID_UNIT
    top = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((right, top)),
             color_for_cv2(line_color),
             thickness=LINE_THICKNESS)
    # 垂直線部
    left = (column+0.5)*GRID_UNIT
    top = (row+0.5)*GRID_UNIT
    bottom = (row+1)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((left, bottom)),
             color_for_cv2(line_color),
             thickness=LINE_THICKNESS)


def draw_right_top_corner(canvas, column, row, line_color):
    """┐描画"""
    # 水平線部
    left = (column+0)*GRID_UNIT
    right = (column+0.5)*GRID_UNIT
    top = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((right, top)),
             color_for_cv2(line_color),
             thickness=LINE_THICKNESS)
    # 垂直線部
    left = (column+0.5)*GRID_UNIT
    top = (row+0.5)*GRID_UNIT
    bottom = (row+1)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((left, bottom)),
             color_for_cv2(line_color),
             thickness=LINE_THICKNESS)


def draw_right_bottom_corner(canvas, column, row, line_color):
    """┘描画"""
    # 水平線部
    left = (column+0)*GRID_UNIT
    right = (column+0.5)*GRID_UNIT
    top = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((right, top)),
             color_for_cv2(line_color),
             thickness=LINE_THICKNESS)
    # 垂直線部
    left = (column+0.5)*GRID_UNIT
    top = (row+0)*GRID_UNIT
    bottom = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((left, bottom)),
             color_for_cv2(line_color),
             thickness=LINE_THICKNESS)


def draw_left_bottom_corner(canvas, column, row, line_color):
    """└描画"""
    # 水平線部
    left = (column+0.5)*GRID_UNIT
    right = (column+1)*GRID_UNIT
    top = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((right, top)),
             color_for_cv2(line_color),
             thickness=LINE_THICKNESS)
    # 垂直線部
    left = (column+0.5)*GRID_UNIT
    top = (row+0)*GRID_UNIT
    bottom = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((left, bottom)),
             color_for_cv2(line_color),
             thickness=LINE_THICKNESS)


def draw_up_tee(canvas, column, row, line_color):
    """┴描画"""
    # 水平線部
    left = (column+0)*GRID_UNIT
    right = (column+1)*GRID_UNIT
    top = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((right, top)),
             color_for_cv2(line_color),
             thickness=LINE_THICKNESS)
    # 垂直線部
    left = (column+0.5)*GRID_UNIT
    top = (row+0)*GRID_UNIT
    bottom = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((left, bottom)),
             color_for_cv2(line_color),
             thickness=LINE_THICKNESS)


def draw_right_tee(canvas, column, row, line_color):
    """├描画"""
    # 水平線部
    left = (column+0.5)*GRID_UNIT
    right = (column+1)*GRID_UNIT
    top = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((right, top)),
             color_for_cv2(line_color),
             thickness=LINE_THICKNESS)
    # 垂直線部
    left = (column+0.5)*GRID_UNIT
    top = (row+0)*GRID_UNIT
    bottom = (row+1)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((left, bottom)),
             color_for_cv2(line_color),
             thickness=LINE_THICKNESS)


def draw_down_tee(canvas, column, row, line_color):
    """┬描画"""
    # 水平線部
    left = (column+0)*GRID_UNIT
    right = (column+1)*GRID_UNIT
    top = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((right, top)),
             color_for_cv2(line_color),
             thickness=LINE_THICKNESS)
    # 垂直線部
    left = (column+0.5)*GRID_UNIT
    top = (row+0.5)*GRID_UNIT
    bottom = (row+1)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((left, bottom)),
             color_for_cv2(line_color),
             thickness=LINE_THICKNESS)


def draw_left_tee(canvas, column, row, line_color):
    """┤描画"""
    # 水平線部
    left = (column+0)*GRID_UNIT
    right = (column+0.5)*GRID_UNIT
    top = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((right, top)),
             color_for_cv2(line_color),
             thickness=LINE_THICKNESS)
    # 垂直線部
    left = (column+0.5)*GRID_UNIT
    top = (row+0)*GRID_UNIT
    bottom = (row+1)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((left, bottom)),
             color_for_cv2(line_color),
             thickness=LINE_THICKNESS)


def draw_left_top_round_corner(canvas, column, row, line_color):
    """┌描画（丸み）"""
    # 曲線
    right = (column+1)*GRID_UNIT
    bottom = (row+1)*GRID_UNIT
    cv2.ellipse(canvas,
                point_for_cv2((right, bottom)),
                point_for_cv2((GRID_UNIT/2, GRID_UNIT/2)),
                0,
                180,  # yが逆さの座標系
                270,
                color_for_cv2(line_color),
                thickness=LINE_THICKNESS,
                lineType=2)


def draw_right_top_round_corner(canvas, column, row, line_color):
    """┐描画（丸み）"""
    # 曲線
    left = column*GRID_UNIT
    bottom = (row+1)*GRID_UNIT
    cv2.ellipse(canvas,
                point_for_cv2((left, bottom)),
                point_for_cv2((GRID_UNIT/2, GRID_UNIT/2)),
                0,
                270,  # yが逆さの座標系
                360,
                color_for_cv2(line_color),
                thickness=LINE_THICKNESS,
                lineType=2)


def draw_right_bottom_round_corner(canvas, column, row, line_color):
    """┘描画（丸み）"""
    # 曲線
    left = column*GRID_UNIT
    top = row*GRID_UNIT
    cv2.ellipse(canvas,
                point_for_cv2((left, top)),
                point_for_cv2((GRID_UNIT/2, GRID_UNIT/2)),
                0,
                0,  # yが逆さの座標系
                90,
                color_for_cv2(line_color),
                thickness=LINE_THICKNESS,
                lineType=2)


def draw_left_bottom_round_corner(canvas, column, row, line_color):
    """└描画（丸み）"""
    # 曲線
    right = (column+1)*GRID_UNIT
    top = row*GRID_UNIT
    cv2.ellipse(canvas,
                point_for_cv2((right, top)),
                point_for_cv2((GRID_UNIT/2, GRID_UNIT/2)),
                0,
                90,  # yが逆さの座標系
                180,
                color_for_cv2(line_color),
                thickness=LINE_THICKNESS,
                lineType=2)


def draw_circle(canvas, column, row, line_color):
    """○ます"""
    # 円
    left = (column+0.5)*GRID_UNIT
    top = (row+0.5)*GRID_UNIT
    cv2.circle(canvas,
               point_for_cv2((left, top)),
               int(GRID_UNIT/2),
               color_for_cv2(line_color),
               thickness=-1)


def draw_cross(canvas, column, row, line_color):
    """×ます"""
    # 円
    left = column*GRID_UNIT
    right = (column+1)*GRID_UNIT
    top = row*GRID_UNIT
    bottom = (row+1)*GRID_UNIT
    # バロック ダイアゴナル
    cv2.line(canvas,
             point_for_cv2((left, bottom)),
             point_for_cv2((right, top)),
             color_for_cv2(line_color),
             thickness=LINE_THICKNESS)
    # シニスター ダイアゴナル
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((right, bottom)),
             color_for_cv2(line_color),
             thickness=LINE_THICKNESS)


def draw_space(canvas, column, row, font_color):
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
             color_for_cv2(font_color),
             thickness=FONT_THICKNESS)
    # 左斜辺
    left2 = (column+0.1)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left2, bottom)),
             point_for_cv2((center, bottom2)),
             color_for_cv2(font_color),
             thickness=FONT_THICKNESS)
    # 右斜辺
    left2 = (column+0.9)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((center, bottom2)),
             point_for_cv2((right, bottom)),
             color_for_cv2(font_color),
             thickness=FONT_THICKNESS)


def draw_up_arrow(canvas, column, row, line_color):
    """↑描画"""
    left = (column+0.5)*GRID_UNIT
    top = (row+0.2)*GRID_UNIT
    bottom = (row+1)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((left, bottom)),
             color_for_cv2(line_color),
             thickness=LINE_THICKNESS)
    # 矢頭
    left2 = (column+0.2)*GRID_UNIT
    top2 = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((left2, top2)),
             color_for_cv2(line_color),
             thickness=LINE_THICKNESS)
    # 矢頭
    left2 = (column+0.8)*GRID_UNIT
    top2 = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((left2, top2)),
             color_for_cv2(line_color),
             thickness=LINE_THICKNESS)


def draw_right_arrow(canvas, column, row, line_color):
    """→描画"""
    left = column*GRID_UNIT
    right = (column+0.8)*GRID_UNIT
    top = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((right, top)),
             color_for_cv2(line_color),
             thickness=LINE_THICKNESS)
    # 矢頭
    right2 = (column+0.5)*GRID_UNIT
    top2 = (row+0.2)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((right, top)),
             point_for_cv2((right2, top2)),
             color_for_cv2(line_color),
             thickness=LINE_THICKNESS)
    # 矢頭
    right2 = (column+0.5)*GRID_UNIT
    top2 = (row+0.8)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((right, top)),
             point_for_cv2((right2, top2)),
             color_for_cv2(line_color),
             thickness=LINE_THICKNESS)


def draw_down_arrow(canvas, column, row, line_color):
    """↓描画"""
    left = (column+0.5)*GRID_UNIT
    top = row*GRID_UNIT
    bottom = (row+0.8)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((left, bottom)),
             color_for_cv2(line_color),
             thickness=LINE_THICKNESS)
    # 矢頭
    left2 = (column+0.2)*GRID_UNIT
    bottom2 = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, bottom)),
             point_for_cv2((left2, bottom2)),
             color_for_cv2(line_color),
             thickness=LINE_THICKNESS)
    # 矢頭
    left2 = (column+0.8)*GRID_UNIT
    bottom2 = (row+0.5)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, bottom)),
             point_for_cv2((left2, bottom2)),
             color_for_cv2(line_color),
             thickness=LINE_THICKNESS)


def draw_left_arrow(canvas, column, row, line_color):
    """←描画"""
    left = (column+0.2)*GRID_UNIT
    right = (column+1)*GRID_UNIT
    top = (row+0.5)*GRID_UNIT
    # 線
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((right, top)),
             color_for_cv2(line_color),
             thickness=LINE_THICKNESS)
    # 矢頭
    left2 = (column+0.5)*GRID_UNIT
    top2 = (row+0.2)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((left2, top2)),
             color_for_cv2(line_color),
             thickness=LINE_THICKNESS)
    # 矢頭
    left2 = (column+0.5)*GRID_UNIT
    top2 = (row+0.8)*GRID_UNIT
    cv2.line(canvas,
             point_for_cv2((left, top)),
             point_for_cv2((left2, top2)),
             color_for_cv2(line_color),
             thickness=LINE_THICKNESS)


def draw_agent(canvas, agent):
    """エージェントの描画"""
    column = agent.location[0]
    row = agent.location[1]
    draw_circle(
        canvas, column, row, AGENT_COLOR)
    draw_jp(canvas, '@', ((column+0.5)*GRID_UNIT, (row+0.5)*GRID_UNIT),
            TRUE_TYPE_FONT, GRID_UNIT, FONT_COLOR)
