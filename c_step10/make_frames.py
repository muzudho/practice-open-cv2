"""png画像を複数枚出力します
"""

import math
import cv2
import numpy as np
from colors import PALE_GRAY, LIGHT_GRAY, BLACK, LIGHT_RED, LIGHT_GREEN, \
    LIGHT_BLUE, RED, GREEN, BLUE
from color_calc import calc_step1, calc_step2, append_rank3_to_color, \
    convert_3heights_to_3bytes, to_be_red, to_be_green, to_be_blue, \
    calc_color_element_rates
from bar_box import BarBox
from circle_rail import CircleRail
from outer_circle import OuterCircle
from conf import GRID_INTERVAL_H, PHASE_COUNTS, FONT_SCALE


# 描画する画像を作る
# 横幅 約500 以上にすると ブログで縮小されて .gif ではなくなるので、横幅を 約500未満にすること（＾～＾）
CANVAS_WIDTH = 285  # crieitブログは少なくとも 横幅 450px なら圧縮されない（＾～＾）
CANVAS_HEIGHT = 186
CHANNELS = 3
# モノクロ背景 0黒→255白
MONO_BACKGROUND = 255

# RGBバー１段目（レールとなる円より上にある）
BAR_TOP1 = 8 * GRID_INTERVAL_H
# 円レール circle rail left
CRAIL_LEFT = 8 * GRID_INTERVAL_H

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
        inner_circle = OuterCircle()
        outer_circle = OuterCircle()
        for _ in range(0, 10):  # Wait frames
            canvas = make_canvas()
            bar_box, _circle_rail, _inner_circle, _outer_circle = make_scene1(
                bar_rates, inner_circle, outer_circle)
            draw_grid(canvas)
            bar_box.draw_outline(canvas)
            bar_box.draw_rank2_box(canvas)
            bar_box.draw_bar_rate_rank2(canvas)  # バー率テキスト
            draw_tone_name(canvas, bar_box, tone_name)
            # 書出し
            canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)  # BGRをRGBにする
            cv2.imwrite(f"./shared/out-cstep4-{seq}.png", canvas)
            seq += 1

        # 描画：色相環のアニメーション表示
        seq, canvas = make_circle(canvas, seq, bar_rates, tone_name)

        for _ in range(0, 10):  # Wait frames
            cv2.imwrite(f"./shared/out-cstep4-{seq}.png", canvas)
            seq += 1


def make_circle(canvas, seq, bar_rates, tone_name):
    """色相環一周分の画像を出力"""

    inner_circle = OuterCircle()
    outer_circle = OuterCircle()

    for phase in range(0, PHASE_COUNTS):
        theta = 360/PHASE_COUNTS*phase
        canvas = make_canvas()
        bar_box, circle_rail, inner_circle, outer_circle = make_scene1(
            bar_rates, inner_circle, outer_circle)
        inner_circle.phase = phase
        outer_circle.phase = phase

        # 円周上の点の位置
        circle_rail.theta = theta

        # バーR
        bar_box.step1_red_bar_rect.left_top = (
            bar_box.red_left, circle_rail.red_p[1])
        bar_box.step1_red_bar_rect.right_bottom = (
            bar_box.red_left+bar_box.one_width, bar_box.top3)
        # バーG
        bar_box.step1_green_bar_rect.left_top = (
            bar_box.green_left, circle_rail.green_p[1])
        bar_box.step1_green_bar_rect.right_bottom = (
            bar_box.green_left+bar_box.one_width, bar_box.top3)
        # バーB
        bar_box.step1_blue_bar_rect.left_top = (
            bar_box.blue_left, circle_rail.blue_p[1])
        bar_box.step1_blue_bar_rect.right_bottom = (
            bar_box.blue_left+bar_box.one_width, bar_box.top3)
#        print(
#            f"red={bar_box.step1_red_bar_rect.debug_string} \
# green={bar_box.step1_green_bar_rect.debug_string} \
# blue={bar_box.step1_blue_bar_rect.debug_string}")

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

        bar_box.addition_3bars_height = (red_add, green_add, blue_add)

        ceil_height = bar_box.ceil_height_rgb_value
        base_line = bar_box.base_line_rgb_value

        # 内環状
        theta = inner_circle.phase * inner_circle.unit_arc
        color = calc_step1(theta)
        inner_color = append_rank3_to_color(color, bar_box.rates)
        inner_circle.color_list.append(inner_color)

        # 外環状
        theta = outer_circle.phase * outer_circle.unit_arc
        color = calc_step1(theta)
        outer_color = append_rank3_to_color(color, bar_box.rates)
        outer_upper_bound = outer_circle.get_upper_bound_value(bar_box.rates)
        outer_color = calc_step2(outer_color, outer_upper_bound,
                                 255, ceil_height, base_line)
        outer_circle.color_list.append(outer_color)
        #

        draw_grid(canvas)  # 罫線
        bar_box.draw_outline(canvas)  # 箱の輪郭
        canvas = draw_canvas(canvas, bar_box, circle_rail,
                             inner_circle, outer_circle)
        bar_box.draw_rank2_box(canvas)
        draw_tone_name(canvas, bar_box, tone_name)

        # 書出し
        canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)  # BGRをRGBにする
        cv2.imwrite(f"./shared/out-cstep4-{seq}.png", canvas)
        seq += 1

    return seq, canvas


def make_canvas():
    """キャンバス生成"""
    return np.full((CANVAS_HEIGHT, CANVAS_WIDTH, CHANNELS),
                   MONO_BACKGROUND, dtype=np.uint8)


def make_scene1(bar_rates, inner_circle, outer_circle):
    """オブジェクトの位置とキャンバスを返します
    """

    bar_box = BarBox()
    circle_rail = CircleRail()

    # バー
    # RGBバーの１段目、２段目、３段目の高さ（２０分率）
    bar_box.top1 = BAR_TOP1
    bar_box.rates = bar_rates
    bar_box.height1 = int(bar_box.rates[0] * 20 * GRID_INTERVAL_H)
    bar_box.height2 = int(bar_box.rates[1] * 20 * GRID_INTERVAL_H)
    bar_box.height3 = int(bar_box.rates[2] * 20 * GRID_INTERVAL_H)
    bar_box.one_width = 30  # フォント１文字の横幅が 10 と想定
    bar_box.rate_text_gap = int(0.5*GRID_INTERVAL_H)
    # 円レール
    circle_rail.range = int(bar_box.height2 / 2)

    # バー箱の左
    range_width = 10
    outer_circle_margin = 3
    width = 2 * (range_width + outer_circle_margin)
    bar_box.left = int(CRAIL_LEFT + width*GRID_INTERVAL_H +
                       2*int(1.5*GRID_INTERVAL_H))
    # バーの筋
    bar_box.font_scale = FONT_SCALE
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
    inner_circle.origin = (circle_rail.center[0], circle_rail.center[1])
    outer_circle.origin = (circle_rail.center[0], circle_rail.center[1])
    circle_rail.point_range = 4
    # RGBバー２段目
    bar_box.top2 = circle_rail.top
    bar_box.rank1_rect.left_top = (bar_box.left, BAR_TOP1)
    bar_box.rank1_rect.right_bottom = (bar_box.right, bar_box.top2)
    # バー２段目（レールとなる円と水平線を合わす）
    bar_box.top3 = bar_box.top2 + bar_box.height2
    bar_box.bottom = bar_box.top3 + bar_box.height3
    bar_box.height = bar_box.height1 + bar_box.height2 + bar_box.height3
    # RGBバー２段目領域
    bar_box.rank2_rect.left_top = (bar_box.left, bar_box.top2)
    bar_box.rank2_rect.right_bottom = (bar_box.right, bar_box.top3)
    # RGBバー３段目
    bar_box.rank3_rect.left_top = (bar_box.left, bar_box.top3)
    bar_box.rank3_rect.right_bottom = (bar_box.right, bar_box.bottom)

    inner_circle.area_size = (circle_rail.range + 2*GRID_INTERVAL_H+int(1.6*GRID_INTERVAL_H),
                              circle_rail.range + 2*GRID_INTERVAL_H+int(1.6*GRID_INTERVAL_H))
    inner_circle.phases = PHASE_COUNTS
    outer_circle.area_size = (circle_rail.range + 2*GRID_INTERVAL_H+3*GRID_INTERVAL_H,
                              circle_rail.range + 2*GRID_INTERVAL_H+3*GRID_INTERVAL_H)
    outer_circle.phases = PHASE_COUNTS

    return bar_box, circle_rail, inner_circle, outer_circle


def draw_grid(canvas):
    """背景に罫線を引きます"""
    # 水平線グリッド
    for i in range(0, int(CANVAS_HEIGHT/GRID_INTERVAL_H)+1):
        if i % 2 == 0:  # ファイルサイズ削減のため間引き
            y_num = GRID_INTERVAL_H*i
            cv2.line(canvas, (0, y_num), (CANVAS_WIDTH, y_num),
                     PALE_GRAY, thickness=1)


def draw_tone_name(canvas, bar_box, tone_name):
    """トーン名を描きます"""
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = FONT_SCALE
    line_type = 2
    cv2.putText(canvas,
                f"{tone_name}",
                (bar_box.left, BAR_TOP1-3*GRID_INTERVAL_H),  # x,y
                font,
                font_scale,
                BLACK,
                line_type)


def draw_canvas(canvas, bar_box, circle_rail, inner_circle, outer_circle):
    """アニメの１コマを作成します"""

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

    # 1色成分
    a_color = convert_3heights_to_3bytes(
        bar_box.addition_3bars_height, bar_box.height)
    step1_color = convert_3heights_to_3bytes(
        bar_box.create_step1_3bars_height(), bar_box.height)
    rank3_color = convert_3heights_to_3bytes(
        bar_box.create_rank3_3bars_height(), bar_box.height)
    rank23_color = convert_3heights_to_3bytes(
        bar_box.create_rank23_3bars_height(), bar_box.height)
    rank23a_color = convert_3heights_to_3bytes(
        bar_box.create_rank23a_3bars_height(), bar_box.height)
    # 3色成分
    a_3colors = (to_be_red(a_color), to_be_green(a_color), to_be_blue(a_color))
    step1_3colors = (to_be_red(step1_color), to_be_green(
        step1_color), to_be_blue(step1_color))
    rank3_3colors = (to_be_red(rank3_color), to_be_green(
        rank3_color), to_be_blue(rank3_color))
    rank23a_3colors = (to_be_red(rank23a_color), to_be_green(
        rank23a_color), to_be_blue(rank23a_color))
    # 成分から角度を逆算
    element_rates, expected_theta = calc_color_element_rates(rank23_color)
    if circle_rail.theta != expected_theta:
        print(
            f"theta={circle_rail.theta:>6.2f}~{expected_theta:>6.2f} \
color_element(rank23_color)=({element_rates[0]:>6.2f}, \
{element_rates[1]:>6.2f}, \
{element_rates[2]:>6.2f})")
    bar_box.draw_bars(canvas, a_3colors, step1_3colors, rank3_3colors)  # RGBバー

    # 色見本 筆算の線
    line_left = bar_box.left - 12*GRID_INTERVAL_H
    line_right = bar_box.right + 4*GRID_INTERVAL_H
    line_top = bar_box.bottom+int(13*GRID_INTERVAL_H)
    cv2.line(canvas, (line_left, line_top),
             (line_right, line_top), LIGHT_GRAY, thickness=2)

    # プラス記号
    color_example_width = 3*GRID_INTERVAL_H
    color_example_left = int(bar_box.left - 1.5 * color_example_width)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = FONT_SCALE
    line_type = 2
    cv2.putText(canvas,
                "+",
                (int(bar_box.left - 3.5 * color_example_width),
                 int(bar_box.bottom+11.5*GRID_INTERVAL_H)),  # x,y
                font,
                font_scale,
                BLACK,
                line_type)

    # 色見本 a
    left_top = (color_example_left, int(
        bar_box.bottom+1*GRID_INTERVAL_H))
    right_bottom = (left_top[0]+color_example_width,
                    left_top[1]+color_example_width)
    cv2.rectangle(canvas, left_top,
                  right_bottom, a_color, thickness=-1)  # 色見本

    # 色見本 step1
    left_top = (color_example_left, int(
        bar_box.bottom+5*GRID_INTERVAL_H))
    right_bottom = (left_top[0]+color_example_width,
                    left_top[1]+color_example_width)
    cv2.rectangle(canvas, left_top,
                  right_bottom, step1_color, thickness=-1)  # 色見本

    # 色見本 3
    left_top = (color_example_left, int(
        bar_box.bottom+9*GRID_INTERVAL_H))
    right_bottom = (left_top[0]+color_example_width,
                    left_top[1]+color_example_width)
    cv2.rectangle(canvas, left_top,
                  right_bottom, rank3_color, thickness=-1)  # 色見本

    # 色見本 23a
    left_top = (color_example_left, int(
        bar_box.bottom+int(14.5*GRID_INTERVAL_H)))
    right_bottom = (left_top[0]+color_example_width,
                    left_top[1]+color_example_width)
    cv2.rectangle(canvas, left_top,
                  right_bottom, rank23a_color, thickness=-1)  # 色見本

    bar_box.draw_bar_rate_rank13(canvas)  # バー率テキスト
    bar_box.draw_bar_rate_rank2(canvas)  # バー率テキスト

    # 色成分数
    bar_box.draw_rgb_number(canvas,
                            a_color, a_3colors,
                            step1_color, step1_3colors,
                            rank3_color, rank3_3colors,
                            rank23a_color, rank23a_3colors)

    # 時計の針
    clock_hand_len = 7*GRID_INTERVAL_H
    inner_p = (
        int(circle_rail.range * math.cos(math.radians(circle_rail.theta-90)) +
            circle_rail.center[0]),
        int(circle_rail.range * math.sin(math.radians(circle_rail.theta-90))+circle_rail.center[1]))
    outer_p = (
        int((circle_rail.range+clock_hand_len) *
            math.cos(math.radians(circle_rail.theta-90))+circle_rail.center[0]),
        int((circle_rail.range+clock_hand_len) * math.sin(math.radians(circle_rail.theta-90))
            + circle_rail.center[1]))
    cv2.line(canvas, inner_p, outer_p, LIGHT_GRAY, thickness=2)

    # 水平線R
    # 線、描画する画像を指定、座標1点目、2点目、色、線の太さ
    cv2.line(canvas, circle_rail.red_p,
             (bar_box.step1_red_bar_rect.right_bottom[0],
              circle_rail.red_p[1]),
             LIGHT_RED, thickness=2)

    # 水平線G
    cv2.line(canvas, circle_rail.green_p,
             (bar_box.step1_green_bar_rect.right_bottom[0],
              circle_rail.green_p[1]),
             LIGHT_GREEN, thickness=2)

    # 水平線B
    cv2.line(canvas, circle_rail.blue_p,
             (bar_box.step1_blue_bar_rect.right_bottom[0],
              circle_rail.blue_p[1]),
             LIGHT_BLUE, thickness=2)

    inner_circle.draw_me(canvas)  # 内環状
    outer_circle.draw_me(canvas)  # 外環状

    # cv2.imshow('Title', canvas)
    # cv2.imwrite('form.jpg',canvas)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return canvas


main()
