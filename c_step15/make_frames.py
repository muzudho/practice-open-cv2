"""png画像を複数枚出力します
"""

import math
import cv2
import numpy as np
from colors import WHITE, PALE_GRAY, BLACK,  \
    SOFT_GRAY, RED, GREEN, BLUE, \
    DARK_GRAYISH_BLACK
from color_calc import calc_step2, \
    convert_3heights_to_3bytes
from bar_box import BarBox
from circle_rail import CircleRail
from outer_circle import OuterCircle
from conf import GRID_UNIT, PHASE_COUNTS, FONT_SCALE


# 描画する画像を作る
# 横幅 約500 以上にすると ブログで縮小されて .gif ではなくなるので、横幅を 約500未満にすること（＾～＾）
CANVAS_WIDTH = 540  # crieitブログは少なくとも 横幅 450px なら圧縮されない（＾～＾）
CANVAS_HEIGHT = 320
CHANNELS = 3
# モノクロ背景 0黒→255白 178=SOFT_GRAY
MONO_BACKGROUND = SOFT_GRAY[0]

# RGBバー１段目（レールとなる円より上にある）
BAR_TOP1 = 7 * GRID_UNIT
# 箱の左
BAR_BOX_LEFT = int(22 * GRID_UNIT)
# 円の中心と、箱の左との距離
CIRCLE_DISTANCE = int(13.5 * GRID_UNIT)

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
    'Bright zone',
    'Strong zone',
    'Deep zone',
    'Light zone',
    'Soft zone',
    'Dull zone',
    'Dark zone',
    'Pale zone',
    'Light grayish zone',
    'Grayish zone',
    'Dark grayish zone',
    'Vivid zone',  # Cosine curve
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
            bar_box, _circle_rail, _outer_circle = make_scene1(
                bar_rates, outer_circle)
            draw_grid(canvas)
            bar_box.draw_outline(canvas)
            bar_box.draw_rank2_box(canvas)
            bar_box.draw_bars_rate(canvas)  # バー率テキスト
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

    outer_circle = OuterCircle()

    for phase in range(0, PHASE_COUNTS):
        theta = 360/PHASE_COUNTS*phase
        canvas = make_canvas()
        bar_box, circle_rail, outer_circle = make_scene1(
            bar_rates, outer_circle)
        outer_circle.phase = phase

        # 円周上の点の位置
        circle_rail.theta = theta

        # バーR
        bar_box.step1_rect[0].left_top = (
            bar_box.red_left, circle_rail.red_p[1])
        bar_box.step1_rect[0].right_bottom = (
            bar_box.red_left+bar_box.one_width, bar_box.top3)
        # バーG
        bar_box.step1_rect[1].left_top = (
            bar_box.green_left, circle_rail.green_p[1])
        bar_box.step1_rect[1].right_bottom = (
            bar_box.green_left+bar_box.one_width, bar_box.top3)
        # バーB
        bar_box.step1_rect[2].left_top = (
            bar_box.blue_left, circle_rail.blue_p[1])
        bar_box.step1_rect[2].right_bottom = (
            bar_box.blue_left+bar_box.one_width, bar_box.top3)
#        print(
#            f"red={bar_box.step1_rect[0].debug_string} \
# green={bar_box.step1_rect[1].debug_string} \
# blue={bar_box.step1_rect[2].debug_string}")

        bar_box.delta_3bars_height = calc_step2(
            bar_box.create_step1_3bars_height(),
            bar_box.height2
        )

        # 外環状
        theta = outer_circle.phase * outer_circle.unit_arc
        outer_color = convert_3heights_to_3bytes(
            bar_box.create_rank23a_3bars_height(), bar_box.height)
        outer_circle.color_list.append(outer_color)
        #

        draw_grid(canvas)  # 罫線
        bar_box.draw_outline(canvas)  # 箱の輪郭
        canvas = draw_canvas(canvas, bar_box, circle_rail,
                             outer_circle)
        draw_tone_name(canvas, bar_box, tone_name)  # トーン名

        # 書出し
        canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)  # BGRをRGBにする
        cv2.imwrite(f"./shared/out-cstep4-{seq}.png", canvas)
        seq += 1

    return seq, canvas


def make_canvas():
    """キャンバス生成"""
    return np.full((CANVAS_HEIGHT, CANVAS_WIDTH, CHANNELS),
                   MONO_BACKGROUND, dtype=np.uint8)


def make_scene1(bar_rates, outer_circle):
    """オブジェクトの位置とキャンバスを返します
    """

    bar_box = BarBox()
    circle_rail = CircleRail()

    # バー
    # RGBバーの１段目、２段目、３段目の高さ（２０分率）
    bar_box.top1 = BAR_TOP1
    bar_box.rates = bar_rates
    bar_box.height1 = int(bar_box.rates[0] * 10 * GRID_UNIT)
    bar_box.height2 = int(bar_box.rates[1] * 10 * GRID_UNIT)
    bar_box.height3 = int(bar_box.rates[2] * 10 * GRID_UNIT)
    bar_box.one_width = 30  # フォント１文字の横幅が 10 と想定
    bar_box.y_axis_label_gap = int(0.25*GRID_UNIT)
    bar_box.rate_text_gap = int(0.2*GRID_UNIT)
    # 円レール
    circle_rail.range = int(bar_box.height2 / 2)

    # バー箱の左
    bar_box.left = BAR_BOX_LEFT
    # バーの筋
    bar_box.font_scale = FONT_SCALE
    bar_box.line_type = 2
    bar_box.font = cv2.FONT_HERSHEY_SIMPLEX
    bar_box.red_left = bar_box.left
    bar_box.green_left = bar_box.red_left + bar_box.one_width
    bar_box.blue_left = bar_box.green_left + bar_box.one_width
    bar_box.right = bar_box.blue_left + bar_box.one_width
    # レールとなる円 circle rail
    circle_rail.top = BAR_TOP1 + bar_box.height1

    circle_rail.center = (bar_box.left - CIRCLE_DISTANCE,
                          circle_rail.top+circle_rail.range)  # x, y
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
    # print(f"bar_box.height={bar_box.height}")
    # RGBバー２段目領域
    bar_box.rank2_rect.left_top = (bar_box.left, bar_box.top2)
    bar_box.rank2_rect.right_bottom = (bar_box.right, bar_box.top3)
    # RGBバー３段目
    bar_box.rank3_rect.left_top = (bar_box.left, bar_box.top3)
    bar_box.rank3_rect.right_bottom = (bar_box.right, bar_box.bottom)

    outer_circle.area_size = (int(7*GRID_UNIT),
                              int(7*GRID_UNIT))
    outer_circle.phases = PHASE_COUNTS

    return bar_box, circle_rail, outer_circle


def draw_grid(_canvas):
    """背景に罫線を引きます。あくまで開発用"""
    # 水平線グリッド
    # for i in range(0, int(CANVAS_HEIGHT/(GRID_UNIT/2))+1):
    #    y_num = GRID_UNIT*i
    #    cv2.line(canvas, (0, y_num), (CANVAS_WIDTH, y_num),
    #             PALE_GRAY, thickness=1)


def draw_tone_name(canvas, bar_box, tone_name):
    """トーン名を描きます"""
    line_type = 2
    cv2.putText(canvas,
                f"{tone_name}",
                (bar_box.left, int(BAR_TOP1-2.5*GRID_UNIT)),  # x,y
                cv2.FONT_HERSHEY_SIMPLEX,
                FONT_SCALE,
                DARK_GRAYISH_BLACK,
                line_type)


def draw_canvas(canvas, bar_box, circle_rail, outer_circle):
    """アニメの１コマを作成します"""

    circle_rail.draw_me(canvas)  # 円レール

    circle_rail.draw_red_p(canvas)  # 円周上の点R
    circle_rail.draw_green_p(canvas)  # 円周上の点G
    circle_rail.draw_blue_p(canvas)  # 円周上の点B

    # 円に内接する線。三角形
    cv2.line(canvas, circle_rail.red_p,
             circle_rail.green_p, WHITE, thickness=2)
    cv2.line(canvas, circle_rail.green_p,
             circle_rail.blue_p, WHITE, thickness=2)
    cv2.line(canvas, circle_rail.blue_p,
             circle_rail.red_p, WHITE, thickness=2)

    # 1色成分 (高さから 255 へ丸めるとき、誤差が出る)
    rank23d_color = convert_3heights_to_3bytes(
        bar_box.create_rank23a_3bars_height(), bar_box.height)

#    # (WIP) 成分から角度を逆算
#    element_rates, expected_theta = calc_color_element_rates(rank23_color)
#    if circle_rail.theta != expected_theta:
#        print(
#            f"theta={circle_rail.theta:>7.3f}~{expected_theta:>7.3f} \
# color_element(rank23_color)=({element_rates[0]:>7.3f}, \
# {element_rates[1]:>7.3f}, \
# {element_rates[2]:>7.3f})")
    bar_box.draw_3bars(canvas)  # RGBバー

    bar_box.draw_y_axis_label(canvas)  # バー率テキスト

    # 水平線R
    # 線、描画する画像を指定、座標1点目、2点目、色、線の太さ
    cv2.line(canvas, circle_rail.red_p,
             (bar_box.step1_rect[0].left_top[0],
              circle_rail.red_p[1]),
             RED, thickness=2)

    # 水平線G
    cv2.line(canvas, circle_rail.green_p,
             (bar_box.step1_rect[1].left_top[0],
              circle_rail.green_p[1]),
             GREEN, thickness=2)

    # 水平線B
    cv2.line(canvas, circle_rail.blue_p,
             (bar_box.step1_rect[2].left_top[0],
              circle_rail.blue_p[1]),
             BLUE, thickness=2)

    outer_circle.draw_me(canvas)  # 外環状

    # 時計の針
    inner_range = circle_rail.range
    second_range = int(5.5*GRID_UNIT)
    third_range = int(6.5*GRID_UNIT)
    fourth_range = int(7.5*GRID_UNIT)
    inner_p = (
        int(inner_range * math.cos(math.radians(circle_rail.theta-90)) +
            circle_rail.center[0]),
        int(inner_range * math.sin(math.radians(circle_rail.theta-90))+circle_rail.center[1]))
    outer_p = (
        int(second_range *
            math.cos(math.radians(circle_rail.theta-90))+circle_rail.center[0]),
        int(second_range * math.sin(math.radians(circle_rail.theta-90))
            + circle_rail.center[1]))
    cv2.line(canvas, inner_p, outer_p, PALE_GRAY, thickness=2)
    #
    inner_p = (
        int(second_range * math.cos(math.radians(circle_rail.theta-90)) +
            circle_rail.center[0]),
        int(second_range * math.sin(math.radians(circle_rail.theta-90))+circle_rail.center[1]))
    outer_p = (
        int((third_range) *
            math.cos(math.radians(circle_rail.theta-90))+circle_rail.center[0]),
        int((third_range) * math.sin(math.radians(circle_rail.theta-90))
            + circle_rail.center[1]))
    cv2.line(canvas, inner_p, outer_p, WHITE, thickness=2)
    #
    inner_p = (
        int(third_range * math.cos(math.radians(circle_rail.theta-90)) +
            circle_rail.center[0]),
        int(third_range * math.sin(math.radians(circle_rail.theta-90))+circle_rail.center[1]))
    outer_p = (
        int(fourth_range *
            math.cos(math.radians(circle_rail.theta-90))+circle_rail.center[0]),
        int(fourth_range * math.sin(math.radians(circle_rail.theta-90))
            + circle_rail.center[1]))
    cv2.line(canvas, inner_p, outer_p, BLACK, thickness=2)
    #

    # バー箱の２段目の黒枠
    bar_box.draw_rank2_box(canvas)

    # 色成分数
    bar_box.draw_rgb_number(canvas,
                            rank23d_color)

    # debug
    # cv2.putText(canvas,
    #            # f"delta_color=({delta_color[0]}, {delta_color[1]}, {delta_color[2]})",
    #            f"delta_3bars_height=({bar_box.delta_3bars_height[0]}, \
    # {bar_box.delta_3bars_height[1]}, \
    # {bar_box.delta_3bars_height[2]})",
    #            (10, 10),  # x,y
    #            cv2.FONT_HERSHEY_SIMPLEX,
    #            FONT_SCALE,
    #            BLACK,
    #            lineType=2)

    # cv2.imshow('Title', canvas)
    # cv2.imwrite('form.jpg',canvas)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return canvas


main()
