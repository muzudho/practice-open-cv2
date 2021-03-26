"""png画像を複数枚出力します
"""

import cv2
import numpy as np
from colors import PALE_GRAY, BLACK, RED, GREEN, BLUE, LIGHT_RED, LIGHT_GREEN, LIGHT_BLUE
from color_calc import calc_step2, calc_color
from bar_box import BarBox
from circle_rail import CircleRail
from brush_point import BrushPoint
from outer_circle import OuterCircle
from conf import GRID_INTERVAL_H, PHASE_COUNTS


# 描画する画像を作る
# 横幅 約500 以上にすると ブログで縮小されて .gif ではなくなるので、横幅を 約500未満にすること（＾～＾）
CANVAS_WIDTH = 450
CANVAS_HEIGHT = 280
CHANNELS = 3
# モノクロ背景 0黒→255白
MONO_BACKGROUND = 255

# RGBバー１段目（レールとなる円より上にある）
BAR_TOP1 = 6 * GRID_INTERVAL_H
# 円レール circle rail left
CRAIL_LEFT = 6 * GRID_INTERVAL_H

# とりあえず 11トーン
BAR_RATES = [
    # 鮮やかさ2番
    [0.1, 0.7, 0.2],  # Bright
    [0.2, 0.7, 0.1],  # Strong
    [0.3, 0.7, 0.0],  # Deep
    # 鮮やかさ3番
    [0.0, 0.4, 0.6],  # Light
    [0.1, 0.4, 0.5],  # Soft
    [0.3, 0.4, 0.3],  # Dull
    [0.4, 0.4, 0.2],  # Dark
    # 鮮やかさ4番
    [0.0, 0.3, 0.7],  # Pale
    [0.2, 0.3, 0.5],  # Light grayish
    [0.4, 0.3, 0.3],  # Grayish
    [0.6, 0.3, 0.1],  # Dark grayish
    # 鮮やかさ1番
    [0.0, 1.0, 0.0],  # Vivid
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
    'Vivid',  # Cosine curve
]


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
        outer_circle = OuterCircle()
        for _ in range(0, 10):  # Wait frames
            canvas = make_canvas()
            bar_box, _circle_rail, _brush_point, _outer_circle = make_scene1(
                bar_rates, outer_circle)
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

    outer_circle = OuterCircle()

    for phase in range(0, PHASE_COUNTS):
        theta = 360/PHASE_COUNTS*phase
        canvas = make_canvas()
        bar_box, circle_rail, brush_point, outer_circle = make_scene1(
            bar_rates, outer_circle)
        outer_circle.phase = phase

        # 円周上の点の位置
        circle_rail.set_theta(theta)
        brush_point.set_theta(theta)

        # バーR
        bar_box.step1_red_bar_p1 = (bar_box.red_left, circle_rail.red_p[1])
        bar_box.step1_red_bar_p2 = (
            bar_box.red_left+bar_box.one_width, bar_box.top3)
        # バーG
        bar_box.step1_green_bar_p1 = (
            bar_box.green_left, circle_rail.green_p[1])
        bar_box.step1_green_bar_p2 = (
            bar_box.green_left+bar_box.one_width, bar_box.top3)
        # バーB
        bar_box.step1_blue_bar_p1 = (bar_box.blue_left, circle_rail.blue_p[1])
        bar_box.step1_blue_bar_p2 = (
            bar_box.blue_left+bar_box.one_width, bar_box.top3)

        upper_bound_px = bar_box.get_step1_upper_bound_y()
        longest_rank2_bar_height = bar_box.top3 - upper_bound_px
        # print(
        #    f"longest_rank2_bar_height={longest_rank2_bar_height} bar_box.height={bar_box.height}")
        zoom = longest_rank2_bar_height / bar_box.height2
        # print(f"zoom={zoom}")
        red_add = int(bar_box.red_step1_height / zoom) - \
            bar_box.red_step1_height
        green_add = int(bar_box.green_step1_height / zoom) - \
            bar_box.green_step1_height
        blue_add = int(bar_box.blue_step1_height / zoom) - \
            bar_box.blue_step1_height
        #print(f"red_add={red_add} green_add={green_add} blue_add={blue_add}")

        bar_box.red_addition = red_add
        bar_box.green_addition = green_add
        bar_box.blue_addition = blue_add

        # バーR追加部分
        bar_box.addition_red_bar_p1 = (
            bar_box.red_left, bar_box.step1_red_bar_p1[1]-bar_box.red_addition)  # yは逆さ
        bar_box.addition_red_bar_p2 = (
            bar_box.red_left+bar_box.one_width, circle_rail.red_p[1])
        # バーG追加部分
        bar_box.addition_green_bar_p1 = (
            bar_box.green_left, bar_box.step1_green_bar_p1[1]-bar_box.green_addition)
        bar_box.addition_green_bar_p2 = (
            bar_box.green_left+bar_box.one_width, circle_rail.green_p[1])
        # バーB追加部分
        bar_box.addition_blue_bar_p1 = (
            bar_box.blue_left, bar_box.step1_blue_bar_p1[1]-bar_box.blue_addition)
        bar_box.addition_blue_bar_p2 = (
            bar_box.blue_left+bar_box.one_width, circle_rail.blue_p[1])

        # 外環状
        ceil_height = bar_box.ceil_height_rgb_value
        base_line = bar_box.base_line_rgb_value
        # upper_bound_value = max(color[0], color[1], color[2])
        # step2_color = calc_step2(
        #    color, upper_bound_value, 255, ceil_height, base_line)
        theta = outer_circle.phase * outer_circle.unit_arc
        out_color = calc_color(theta, bar_box.rates)
        upper_bound = max(out_color[0], out_color[1], out_color[2])
        # print(f"upper_bound={upper_bound}")
        out_color = calc_step2(out_color, upper_bound,
                               255, ceil_height, base_line)
        outer_circle.color_list.append(out_color)
        #

        draw_grid(canvas)
        bar_box.draw_outline(canvas)
        canvas = draw_canvas(canvas, bar_box, circle_rail, brush_point,
                             outer_circle)
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


def make_scene1(bar_rates, outer_circle):
    """オブジェクトの位置とキャンバスを返します
    """

    bar_box = BarBox()
    circle_rail = CircleRail()
    brush_point = BrushPoint()

    # バー
    # RGBバーの１段目、２段目、３段目の高さ（２０分率）
    bar_box.top1 = BAR_TOP1
    bar_box.rates = bar_rates
    bar_box.height1 = int(bar_box.rates[0] * 20 * GRID_INTERVAL_H)
    bar_box.height2 = int(bar_box.rates[1] * 20 * GRID_INTERVAL_H)
    bar_box.height3 = int(bar_box.rates[2] * 20 * GRID_INTERVAL_H)
    bar_box.one_width = 36  # フォント１文字の横幅が 12 と想定
    bar_box.rate_text_gap = int(bar_box.one_width/2)
    # 円レール
    circle_rail.range = int(bar_box.height2 / 2)
    # 塗った円
    brush_point.distance = circle_rail.range + 2*GRID_INTERVAL_H
    brush_point.range = int(1.5*GRID_INTERVAL_H)

    # バー箱の左
    range_width = 10
    outer_circle_margin = 2
    width = 2 * (range_width + outer_circle_margin)
    bar_box.left = int(CRAIL_LEFT + width*GRID_INTERVAL_H +
                       2*brush_point.range)
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
    outer_circle.origin = (circle_rail.center[0], circle_rail.center[1])
    circle_rail.point_range = 4
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

    outer_circle.area_size = (brush_point.distance+2*GRID_INTERVAL_H,
                              brush_point.distance+2*GRID_INTERVAL_H)
    outer_circle.phases = PHASE_COUNTS

    return bar_box, circle_rail, brush_point, outer_circle


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


def draw_canvas(canvas, bar_box, circle_rail, brush_point, outer_circle):
    """アニメの１コマを作成します
    """

    circle_rail.draw_me(canvas)  # 円レール

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
             (bar_box.step1_red_bar_p1[0], circle_rail.red_p[1]), LIGHT_RED, thickness=2)

    # 水平線G
    cv2.line(canvas, circle_rail.green_p,
             (bar_box.step1_green_bar_p1[0], circle_rail.green_p[1]), LIGHT_GREEN, thickness=2)

    # 水平線B
    cv2.line(canvas, circle_rail.blue_p,
             (bar_box.step1_blue_bar_p1[0], circle_rail.blue_p[1]), LIGHT_BLUE, thickness=2)

    bar_box.draw_bars(canvas)  # RGBバー

    step1_color = bar_box.create_step1_color()  # step1 色値
    draw_step1_rgb_number(canvas, step1_color, bar_box)  # step1 RGB値テキスト

    step2_color = bar_box.create_step2_color()  # step2 色値
    bar_box.draw_rgb_number(canvas, step2_color)  # step2 RGB値テキスト

    bar_box.draw_bar_rate(canvas)  # バー率テキスト

    ceil_height = bar_box.ceil_height_rgb_value
    base_line = bar_box.base_line_rgb_value
    upper_bound_value = max(step2_color[0], step2_color[1], step2_color[2])
    step2_color = calc_step2(
        step2_color, upper_bound_value, 255, ceil_height, base_line)
    brush_point.draw_me(canvas, step1_color)  # 塗り円

    # 外環状
    outer_circle.draw_me(canvas, bar_box.rates, ceil_height, base_line)  # 外環状

    # cv2.imshow('Title', canvas)
    # cv2.imwrite('form.jpg',canvas)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return canvas


def draw_step1_rgb_number(canvas, color, bar_box):
    """RGB値テキストを描きます"""

    feeling = 13

    # 16進R値テキスト
    cv2.putText(canvas,
                f"{color[0]:02x}",
                (bar_box.step1_red_bar_p1[0]+feeling,
                    bar_box.bottom+3*bar_box.font_height),  # x,y
                bar_box.font,
                bar_box.font_scale,
                LIGHT_RED,
                bar_box.line_type)
    # 10進R値テキスト
    cv2.putText(canvas,
                f"{color[0]:03}",
                (bar_box.step1_red_bar_p1[0],
                    bar_box.bottom+4*bar_box.font_height),  # x,y
                bar_box.font,
                bar_box.font_scale,
                LIGHT_RED,
                bar_box.line_type)

    # 16進G値テキスト
    cv2.putText(canvas,
                f"{color[1]:02x}",
                (bar_box.step1_green_bar_p1[0]+feeling,
                    bar_box.bottom+3*bar_box.font_height),  # x,y
                bar_box.font,
                bar_box.font_scale,
                LIGHT_GREEN,
                bar_box.line_type)
    # 10進G値テキスト
    cv2.putText(canvas,
                f"{color[1]:03}",
                (bar_box.step1_green_bar_p1[0],
                    bar_box.bottom+4*bar_box.font_height),  # x,y
                bar_box.font,
                bar_box.font_scale,
                LIGHT_GREEN,
                bar_box.line_type)

    # 16進B値テキスト
    cv2.putText(canvas,
                f"{color[2]:02x}",
                (bar_box.step1_blue_bar_p1[0]+feeling,
                    bar_box.bottom+3*bar_box.font_height),  # x,y
                bar_box.font,
                bar_box.font_scale,
                LIGHT_BLUE,
                bar_box.line_type)
    # 10進B値テキスト
    cv2.putText(canvas,
                f"{color[2]:03}",
                (bar_box.step1_blue_bar_p1[0],
                    bar_box.bottom+4*bar_box.font_height),  # x,y
                bar_box.font,
                bar_box.font_scale,
                LIGHT_BLUE,
                bar_box.line_type)


main()
