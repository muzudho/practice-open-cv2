"""png画像を複数枚出力します
"""

import cv2
import numpy as np
from color_calc import calc_color
from colors import PALE_GRAY, LIGHT_GRAY, BLACK, RED, GREEN, BLUE
from bar_box import BarBox
from bar_window import BarWindow
from circle_rail import CircleRail
from brush_point import BrushPoint


# 描画する画像を作る
# 横幅 約500 以上にすると ブログで縮小されて .gif ではなくなるので、横幅を 約500未満にすること（＾～＾）
CANVAS_WIDTH = 450
CANVAS_HEIGHT = 230
CHANNELS = 3
# モノクロ背景 0黒→255白
MONO_BACKGROUND = 255

# 水平線グリッド
GRID_INTERVAL_H = 7  # 7とか割り算しにくい数だが面積、ファイル容量削減のため仕方ない（＾～＾）
# RGBバー１段目（レールとなる円より上にある）
BAR_TOP1 = 6 * GRID_INTERVAL_H
# 円レール circle rail left
CRAIL_LEFT = 6 * GRID_INTERVAL_H

# とりあえず 11トーン
BAR_RATES = [
    [0.0, 0.8, 0.2],  # Bright
    [0.2, 0.8, 0.0],  # Strong
    [0.4, 0.6, 0.0],  # Deep
    [0.0, 0.3, 0.7],  # Light
    [0.2, 0.4, 0.4],  # Soft
    [0.3, 0.5, 0.2],  # Dull
    [0.6, 0.4, 0.0],  # Dark
    [0.0, 0.2, 0.8],  # Pale
    [0.1, 0.3, 0.6],  # Light grayish
    [0.4, 0.3, 0.3],  # Grayish
    [0.6, 0.2, 0.2],  # Dark grayish
    [0.0, 1.0, 0.0],  # Cos curve
]
TONE_NAME = [
    'Bright',
    'Strong',
    'Deep',
    'Light',
    'Soft',
    'Dull',
    'Dark',
    'Pale',
    'Light grayish',
    'Grayish',
    'Dark grayish',
    'Cosine curve',
]
# 一周分のフレーム数
FRAME_COUNTS = 24


def main():
    """RGB値の仕組みが分かるgifアニメ画像を出力します
    """

    # 連番
    seq = 0

    size = len(BAR_RATES)
    for i in range(0, size):
        bar_rates = BAR_RATES[i]
        tone_name = TONE_NAME[i]

        # 描画：トーン名と バー箱 の紹介
        for _ in range(0, 10):  # Wait frames
            canvas = make_canvas()
            bar_box, _circle_rail, _brush_point, _bar_window = make_scene1(
                bar_rates)
            draw_grid(canvas)
            bar_box.draw_outline(canvas)
            bar_box.draw_rank2_box(canvas)
            draw_tone_name(canvas, bar_box, tone_name)
            # 書出し
            canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)  # BGRをRGBにする
            cv2.imwrite(f"./shared/out-cstep4-{seq}.png", canvas)
            seq += 1

        # 描画：色相環のアニメーション表示
        seq = make_circle(canvas, seq, bar_rates, tone_name)


def make_circle(canvas, seq, bar_rates, tone_name):
    """色相環一周分の画像を出力"""

    for i in range(0, FRAME_COUNTS):
        theta = 360/FRAME_COUNTS*i
        canvas = make_canvas()
        bar_box, circle_rail, brush_point, bar_window = make_scene1(
            bar_rates)
        # 円周上の点の位置
        circle_rail.set_theta(theta)
        brush_point.set_theta(theta)

        draw_grid(canvas)
        bar_window.draw_outline(canvas)
        bar_box.draw_outline(canvas)
        canvas = draw_canvas(canvas, bar_box, circle_rail, brush_point,
                             bar_window)
        bar_box.draw_rank2_box(canvas)
        draw_tone_name(canvas, bar_box, tone_name)

        # 書出し
        canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)  # BGRをRGBにする
        cv2.imwrite(f"./shared/out-cstep4-{seq}.png", canvas)
        seq += 1

    return seq


def make_canvas():
    """キャンバス生成"""
    return np.full((CANVAS_HEIGHT, CANVAS_WIDTH, CHANNELS),
                   MONO_BACKGROUND, dtype=np.uint8)


def make_scene1(bar_rates):
    """オブジェクトの位置とキャンバスを返します
    """

    bar_box = BarBox()
    bar_window = BarWindow()
    circle_rail = CircleRail()
    brush_point = BrushPoint()

    # バー
    # RGBバーの１段目、２段目、３段目の高さ（２０分率）
    bar_box.top1 = BAR_TOP1
    bar_box.rates = bar_rates
    bar_box.height1 = int(bar_box.rates[0] * 20 * GRID_INTERVAL_H)
    bar_box.height2 = int(bar_box.rates[1] * 20 * GRID_INTERVAL_H)
    bar_box.height3 = int(bar_box.rates[2] * 20 * GRID_INTERVAL_H)
    bar_box.one_width = 24
    # 円レール
    circle_rail.range = int(bar_box.height2 / 2)
    # 塗った円
    brush_point.distance = circle_rail.range + 2*GRID_INTERVAL_H
    brush_point.range = GRID_INTERVAL_H

    # バー箱の左
    bar_window.one_width = 24
    bar_window.interval = 1
    bar_window_space = 3*bar_window.one_width + \
        2*bar_window.interval+4*GRID_INTERVAL_H
    range_width = 10
    outer_circle_margin = 2
    width = 2 * (range_width + outer_circle_margin)
    bar_box.left = int(CRAIL_LEFT + width*GRID_INTERVAL_H +
                       2*brush_point.range+bar_window_space)
    # バーの筋
    bar_box.font_height = 20
    bar_box.font_scale = 0.6
    bar_box.line_type = 2
    bar_box.font = cv2.FONT_HERSHEY_SIMPLEX
    bar_box.red_left = bar_box.left
    bar_box.green_left = bar_box.red_left + bar_box.one_width + 1
    bar_box.blue_left = bar_box.green_left + bar_box.one_width + 1
    bar_box.right = bar_box.blue_left + bar_box.one_width
    # レールとなる円 circle rail
    circle_rail.top = BAR_TOP1 + bar_box.height1
    circle_rail.center = (CRAIL_LEFT+circle_rail.range,
                          circle_rail.top+circle_rail.range)  # x, y
    brush_point.origin = (circle_rail.center[0], circle_rail.center[1])
    circle_rail.point_range = 6
    # RGBバー２段目
    bar_box.top2 = circle_rail.top
    bar_box.rank1_p1 = (bar_box.left, BAR_TOP1)
    bar_box.rank1_p2 = (bar_box.right, bar_box.top2)
    # バー２段目（レールとなる円と水平線を合わす）
    bar_box.top3 = bar_box.top2 + bar_box.height2
    bar_box.bottom = bar_box.top3 + bar_box.height3
    bar_box.height = bar_box.height1 + bar_box.height2 + bar_box.height3
    # RGBバー２段目領域
    bar_box.rank2_p1 = (bar_box.left, bar_box.top2)
    bar_box.rank2_p2 = (bar_box.right, bar_box.top3)
    # RGBバー３段目
    bar_box.rank3_p1 = (bar_box.left, bar_box.top3)
    bar_box.rank3_p2 = (bar_box.right, bar_box.bottom)

    # バー窓の左（円レールが決まった後）
    bar_window.left_top = (
        int(CRAIL_LEFT + width*GRID_INTERVAL_H + 2*brush_point.range),
        circle_rail.top)
    bar_window.right_bottom = (
        bar_window.left_top[0] + 3*bar_window.one_width+2*bar_window.interval,
        circle_rail.top+2*circle_rail.range)

    return bar_box, circle_rail, brush_point, bar_window


def draw_grid(canvas):
    """背景に罫線を引きます"""
    # 水平線グリッド
    for i in range(0, int(CANVAS_HEIGHT/GRID_INTERVAL_H)+1):
        y_num = GRID_INTERVAL_H*i
        cv2.line(canvas, (0, y_num), (CANVAS_WIDTH, y_num),
                 PALE_GRAY, thickness=1)


def draw_tone_name(canvas, bar_box, tone_name):
    """トーン名を描きます"""
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_height = 20
    font_scale = 0.6
    line_type = 2
    cv2.putText(canvas,
                f"{tone_name}",
                (bar_box.left, BAR_TOP1-font_height),  # x,y
                font,
                font_scale,
                BLACK,
                line_type)


def draw_canvas(canvas, bar_box, circle_rail, brush_point, bar_window):
    """アニメの１コマを作成します
    """

    # 円レール。描画する画像を指定、座標（x,y),半径、色、線の太さ（-1は塗りつぶし）
    cv2.circle(canvas, circle_rail.center,
               circle_rail.range, LIGHT_GRAY, thickness=2)

    # バーR
    bar_box.red_bar_p1 = (bar_box.red_left, circle_rail.red_p[1])
    bar_box.red_bar_p2 = (bar_box.red_left+bar_box.one_width, bar_box.bottom)
    # バーG
    bar_box.green_bar_p1 = (bar_box.green_left, circle_rail.green_p[1])
    bar_box.green_bar_p2 = (
        bar_box.green_left+bar_box.one_width, bar_box.bottom)
    # バーB
    bar_box.blue_bar_p1 = (bar_box.blue_left, circle_rail.blue_p[1])
    bar_box.blue_bar_p2 = (bar_box.blue_left+bar_box.one_width, bar_box.bottom)

    circle_rail.draw_red_p(canvas)  # 円周上の点R
    circle_rail.draw_green_p(canvas)  # 円周上の点G
    circle_rail.draw_blue_p(canvas)  # 円周上の点B

    # 円に内接する線。三角形
    cv2.line(canvas, circle_rail.red_p,
             circle_rail.green_p, BLACK, thickness=2)
    cv2.line(canvas, circle_rail.green_p,
             circle_rail.blue_p, BLACK, thickness=2)
    cv2.line(canvas, circle_rail.blue_p,
             circle_rail.red_p, BLACK, thickness=2)

    # 水平線R
    # 線、描画する画像を指定、座標1点目、2点目、色、線の太さ
    cv2.line(canvas, circle_rail.red_p,
             (bar_box.red_left, circle_rail.red_p[1]), RED, thickness=2)

    # 水平線G
    cv2.line(canvas, circle_rail.green_p,
             (bar_box.green_left, circle_rail.green_p[1]), GREEN, thickness=2)

    # 水平線B
    cv2.line(canvas, circle_rail.blue_p,
             (bar_box.blue_left, circle_rail.blue_p[1]), BLUE, thickness=2)

    bar_box.draw_bars(canvas)  # RGBバー

    # 色値
    color = bar_box.create_color(
        circle_rail.red_p[1]-bar_box.top1,
        circle_rail.green_p[1]-bar_box.top1,
        circle_rail.blue_p[1]-bar_box.top1)

    bar_box.draw_rgb_number(canvas, color)  # R値テキスト
    bar_box.draw_bar_rate(canvas)  # バー率テキスト

    # 色円
    brush_point.draw_me(canvas, color)

    # 外環状
    outer_circle(canvas, brush_point.distance, circle_rail.center, bar_box)

    # cv2.imshow('Title', canvas)
    # cv2.imwrite('form.jpg',canvas)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return canvas


def outer_circle(canvas, color_pallete_range, center, bar_box):
    """外環状
    """

    size = 18
    circumference = 360  # 半径１の円の一周の長さ
    unit_arc = circumference/size  # 等分割した１つの弧

    color_list = []
    for i in range(0, size):
        theta = i * unit_arc
        color = calc_color(theta, bar_box.rates)
        color_list.append(color)

    # 色相環
    for i in range(0, size):
        theta = i * unit_arc
        color = color_list[i]
        # print(f"[{i}] color={color}")

        # 円弧
        # 楕円、描画する画像を指定、座標(x,y),xyの半径、角度,色、線の太さ(-1は塗りつぶし)
        box_size = (color_pallete_range+2*GRID_INTERVAL_H,
                    color_pallete_range+2*GRID_INTERVAL_H)
        cv2.ellipse(canvas,
                    center,
                    box_size,
                    -90,
                    theta,
                    theta+unit_arc,
                    color,
                    thickness=int(GRID_INTERVAL_H*3/2))


main()
