"""png画像を複数枚出力します
"""

import math
import cv2
import numpy as np
from cv2_helper import point_for_cv2, color_for_cv2
from rectangle import Rectangle
from clock_hand import ClockHand
from triangle import Triangle
from conf import GRID_UNIT, PHASE_COUNTS, FONT_SCALE, BAR_TICKS, \
    L_M_U_NAME_LIST
from outer_circle import OuterCircle
from circle_rail import CircleRail
from bar_box import BarBox
from color_calc import convert_3bars_to_ticks
from hsv_model_hul_view import to_color, to_hue_angle  # ACCURACY
from colors import \
    SOFT_GRAY, GRAY, RED, GREEN, BLUE, \
    DARK_GRAYISH_GRAY, BLACK
from hul_in_out_test import hue_angle_test  # upper_test, lower_test
from hsv_vs_hul_test import hsv_vs_hul_hue_angle_test

# 描画する画像を作る
# 横幅 約500 以上にすると ブログで縮小されて .gif ではなくなるので、横幅を 約500未満にすること（＾～＾）
CANVAS_WIDTH = 800  # crieitブログは少なくとも 横幅 450px なら圧縮されない（＾～＾） 470px なら圧縮されてしまう（＾～＾）
CANVAS_HEIGHT = 800
CHANNELS = 3

# RGBバー（レールとなる円より上にある）
BAR_BOX_TOP = 6 * GRID_UNIT
# 箱の左
BAR_BOX_LEFT = 18 * GRID_UNIT
# 円の中心と、箱の左との距離
CIRCLE_DISTANCE = 14 * GRID_UNIT


def main():
    """RGB値の仕組みが分かるgifアニメ画像を出力します
    """

    # 連番
    seq = 0

    for (_, record) in enumerate(L_M_U_NAME_LIST):

        # 描画：トーン名と バー箱 の紹介
        outer_circle = OuterCircle()
        for _ in range(0, 10):  # Wait frames
            canvas = make_canvas()
            bar_rate = (record[0], record[1], record[2])
            bar_box, circle_rail, _outer_circle, _inscribed_triangle, _clock_hand = update_scene1(
                bar_rate, outer_circle)
            draw_grid(canvas)
            circle_rail.draw_circle(canvas)  # 円レール
            draw_border(circle_rail, canvas)  # 背景の上限、下限の線
            bar_box.draw_outline(canvas)
            bar_box.draw_rank2_box(canvas)
            bar_box.draw_bars_rate(canvas)  # バー率テキスト
            draw_tone_name(canvas, bar_box, record[3])
            # 書出し
            canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)  # BGRをRGBにする
            cv2.imwrite(f"./@share/out-cstep4-{seq}.png", canvas)
            seq += 1

        # 描画：色相環のアニメーション表示
        seq, canvas = update_circle(canvas, seq, bar_rate, record[3])

        for _ in range(0, 10):  # Wait frames
            cv2.imwrite(f"./@share/out-cstep4-{seq}.png", canvas)
            seq += 1


def update_circle(canvas, seq, bar_rate, tone_name):
    """色相環一周分の画像を出力"""

    outer_circle = OuterCircle()

    for phase in range(0, PHASE_COUNTS):
        canvas = make_canvas()
        bar_box, circle_rail, outer_circle, large_triangle, clock_hand = update_scene1(
            bar_rate, outer_circle)
        error_angle = update_scene1_with_rotate(seq, bar_rate,
                                                phase, bar_box, circle_rail, outer_circle,
                                                large_triangle, clock_hand)

        draw_grid(canvas)  # 罫線
        bar_box.draw_outline(canvas)  # 箱の輪郭
        canvas = draw_canvas(canvas, bar_box, circle_rail,
                             outer_circle, large_triangle, clock_hand, error_angle)
        draw_tone_name(canvas, bar_box, tone_name)  # トーン名

        # 書出し
        canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)  # BGRをRGBにする
        cv2.imwrite(f"./@share/out-cstep4-{seq}.png", canvas)
        seq += 1

    return seq, canvas


def make_canvas():
    """キャンバス生成"""
    return np.full((CANVAS_HEIGHT, CANVAS_WIDTH, CHANNELS),
                   color_for_cv2(SOFT_GRAY, BAR_TICKS)[0], dtype=np.uint8)


def update_scene1(bar_rate, outer_circle):
    """オブジェクトの位置とキャンバスを返します
    """

    # RGBバー
    bar_box = BarBox()
    bar_box.rates = bar_rate
    left_box_width = bar_box.rates[0] * 20 * GRID_UNIT
    middle_box_width = bar_box.rates[1] * 20 * GRID_UNIT
    right_box_width = bar_box.rates[2] * 20 * GRID_UNIT
    bar_box.left = BAR_BOX_LEFT
    bar_box.lower_x = bar_box.left + left_box_width
    bar_box.upper_x = bar_box.lower_x + middle_box_width
    bar_box.right = bar_box.upper_x + right_box_width
    bar_box.top = BAR_BOX_TOP
    bar_box.bottom = bar_box.top + 90
    bar_box.label_gap = -0.75*GRID_UNIT
    bar_box.font_scale = FONT_SCALE
    bar_box.line_type = 2
    bar_box.font = cv2.FONT_HERSHEY_SIMPLEX

    # レールとなる円 circle rail
    circle_rail = CircleRail()
    circle_rail.drawing_top = bar_box.bottom + GRID_UNIT
    circle_rail.drawing_bottom = CANVAS_HEIGHT - GRID_UNIT
    circle_rail.radius = middle_box_width / 2

    circle_rail.center = ((bar_box.lower_x+bar_box.upper_x)/2,
                          bar_box.bottom+CIRCLE_DISTANCE + bar_box.width*4/10)
    circle_rail.border_rect = Rectangle(
        bar_box.lower_x,
        circle_rail.center[1] - circle_rail.radius,
        bar_box.upper_x,
        circle_rail.center[1] + circle_rail.radius)
    circle_rail.point_range = 4

    radius2_expected = bar_box.width*9/10

    # 外環状
    outer_circle.origin = (circle_rail.center[0], circle_rail.center[1])
    outer_circle.radius = radius2_expected
    outer_circle.phases = PHASE_COUNTS
    outer_circle.tickness = 5.0*GRID_UNIT  # 3.0*GRID_UNIT  # 1.5*GRID_UNIT

    # 長方形に内接する大きな正三角形
    large_triangle = Triangle()
    large_triangle.edge_color = GRAY
    large_triangle.nodes_color = (RED, GREEN, BLUE)
    large_triangle.node_radius = GRID_UNIT / 2
    large_triangle.center_color = GRAY

    # 時計の針
    clock_hand = ClockHand()
    clock_hand.center = (circle_rail.center[0], circle_rail.center[1])
    clock_hand.unit_arc = outer_circle.unit_arc
    clock_hand.tickness = 2
    clock_hand.radius1 = circle_rail.radius  # 1st range
    clock_hand.radius2 = radius2_expected - \
        outer_circle.tickness / 2 - clock_hand.tickness  # 2nd range
    clock_hand.radius3 = radius2_expected + \
        outer_circle.tickness / 2 + clock_hand.tickness  # 3rd range

    return bar_box, circle_rail, outer_circle, large_triangle, clock_hand


def update_scene1_with_rotate(
        seq, bar_rate, phase, bar_box, circle_rail, outer_circle,
        large_triangle, clock_hand):
    """回転が伴うモデルを更新"""
    input_angle = math.floor(360/PHASE_COUNTS*phase)
    expected_theta = math.radians(input_angle)

    outer_circle.phase = phase

    # 円周上の点の位置
    circle_rail.theta = expected_theta

    input_color = to_color(bar_rate, expected_theta)

    # バーの横幅に変換
    red = input_color[0]
    green = input_color[1]
    blue = input_color[2]

    # 逆関数のテスト
    # 弧度法
    output_angle, description = to_hue_angle(input_color)
    hul_phase = description[2]

    # 上限値(U)、下限値(L) テスト
    #expected_upper = (bar_box.upper_x - bar_box.left) / bar_box.width
    #expected_lower = (bar_box.lower_x - bar_box.left) / bar_box.width
    #actual_upper = description[0]
    #actual_lower = description[1]
    # 逆関数は合っていて、順関数の方が間違っているケースがある（＾～＾）
    # upper_test(seq, hul_phase, expected_upper, actual_upper,
    #           input_angle, input_color)
    # lower_test(seq, hul_phase, expected_lower, actual_lower,
    #           input_angle, input_color)

    diff_angle = hue_angle_test(
        seq, hul_phase, input_angle, output_angle, input_color)
    hsv_vs_hul_hue_angle_test(
        f"seq={seq:5} hul_phase={hul_phase}", input_color)

    red_bar_width = red * bar_box.width
    green_bar_width = green * bar_box.width
    blue_bar_width = blue * bar_box.width
    # バーR
    bar_box.red_right = bar_box.left + red_bar_width
    # バーG
    bar_box.green_right = bar_box.left + green_bar_width
    # バーB
    bar_box.blue_right = bar_box.left + blue_bar_width

    # 外環状
    theta = math.radians(outer_circle.phase * outer_circle.unit_arc)
    n3bars_width = bar_box.create_3bars_width()
    outer_circle.color_list.append(convert_3bars_to_ticks(
        n3bars_width, bar_box.width))

    # 大三角形
    large_triangle.update(
        bar_box.upper_x, bar_box.lower_x, circle_rail.center, theta, input_color)

    gravity = large_triangle.triangular_center_of_gravity()
    diff_xy = (gravity[0] - circle_rail.center[0],
               gravity[1] - circle_rail.center[1])
    large_triangle.correct_horizon(diff_xy)

    # 時計の針
    clock_hand.theta = theta

    return diff_angle


def draw_grid(_canvas):
    """背景に罫線を引きます。あくまで開発用"""
    # 水平線グリッド
    # for i in range(0, CANVAS_HEIGHT/(GRID_UNIT/2)+1):
    #    y_num = GRID_UNIT*i
    #    cv2.line(canvas, (0, y_num), (CANVAS_WIDTH, y_num),
    #             color_for_cv2(PALE_GRAY, BAR_TICKS), thickness=1)


def draw_tone_name(canvas, bar_box, tone_name):
    """トーン名を描きます"""
    line_type = 2
    cv2.putText(canvas,
                f"{tone_name}",
                point_for_cv2((bar_box.left, BAR_BOX_TOP-3.5*GRID_UNIT)),
                cv2.FONT_HERSHEY_SIMPLEX,
                2*FONT_SCALE,
                color_for_cv2(DARK_GRAYISH_GRAY, BAR_TICKS),
                line_type)


def draw_canvas(canvas, bar_box, circle_rail, outer_circle,
                large_triangle, clock_hand, _error_angle):
    """アニメの１コマを作成します"""

    circle_rail.draw_circle(canvas)  # 円レール
    circle_rail.draw_triangle(canvas)  # 円に内接する正三角形
    draw_border(circle_rail, canvas)  # 背景の上限、下限の線

    large_triangle.draw(canvas)  # 大三角形

    bar_box.draw_3bars(canvas)  # RGBバー

    bar_box.draw_x_axis_label(canvas)  # X軸のラベル

    # 垂直線R
    # 線、描画する画像を指定、座標1点目、2点目、色、線の太さ
    cv2.line(canvas,
             point_for_cv2(large_triangle.nodes_p[0]),
             point_for_cv2((bar_box.red_right, bar_box.red_top)),
             color_for_cv2(RED, BAR_TICKS),
             thickness=2)

    # 垂直線G
    cv2.line(canvas,
             point_for_cv2(large_triangle.nodes_p[2]),  # 青と緑が入れ替わっているのが工夫
             point_for_cv2((bar_box.green_right, bar_box.green_top)),
             color_for_cv2(GREEN, BAR_TICKS),
             thickness=2)

    # 垂直線B
    cv2.line(canvas,
             point_for_cv2(large_triangle.nodes_p[1]),
             point_for_cv2((bar_box.blue_right, bar_box.blue_top)),
             color_for_cv2(BLUE, BAR_TICKS),
             thickness=2)

    outer_circle.draw_me(canvas)  # 外環状

    # 時計の針
    clock_hand.draw_clock_hand(canvas)

    # バー箱の２段目の黒枠
    bar_box.draw_rank2_box(canvas)

    # 色成分数
    bar_box.draw_rgb_number(canvas,
                            convert_3bars_to_ticks(bar_box.create_3bars_width(), bar_box.width))

    # 角度（弧度法）表示
    point_x = (outer_circle.radius/2 + 12*GRID_UNIT) * \
        math.cos(circle_rail.theta) + circle_rail.center[0]
    point_y = (outer_circle.radius/2 + 12*GRID_UNIT) * \
        -math.sin(circle_rail.theta) + circle_rail.center[1]
    cv2.putText(canvas,
                f"{math.degrees(circle_rail.theta):3.0f}",
                point_for_cv2((point_x, point_y)),
                cv2.FONT_HERSHEY_SIMPLEX,
                FONT_SCALE,
                color_for_cv2(BLACK, BAR_TICKS),
                lineType=2)

    return canvas


def draw_border(circle_rail, canvas):
    """背景の左限、右限の線"""

    diameter = 2*circle_rail.radius
    half_height = diameter * math.tan(math.radians(30))

    # 矩形
    left = circle_rail.center[0] - circle_rail.radius
    top = circle_rail.center[1] - half_height
    right = circle_rail.center[0] + circle_rail.radius
    bottom = circle_rail.center[1] + half_height
    cv2.rectangle(canvas,
                  point_for_cv2((left, top)),
                  point_for_cv2((right, bottom)),
                  color_for_cv2(GRAY, BAR_TICKS),
                  thickness=2)

    # 左限の線
    cv2.line(canvas,
             point_for_cv2((circle_rail.center[0] - circle_rail.radius,
                            circle_rail.drawing_top)),
             point_for_cv2((circle_rail.center[0] - circle_rail.radius,
                            circle_rail.drawing_bottom)),
             color_for_cv2(GRAY, BAR_TICKS),
             thickness=2)
    # 右限の線
    cv2.line(canvas,
             point_for_cv2((circle_rail.center[0] + circle_rail.radius,
                            circle_rail.drawing_top)),
             point_for_cv2((circle_rail.center[0] + circle_rail.radius,
                            circle_rail.drawing_bottom)),
             color_for_cv2(GRAY, BAR_TICKS),
             thickness=2)


main()
