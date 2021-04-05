"""png画像を複数枚出力します
"""

import cv2
import numpy as np
from color_hul_model import to_color_rate, inverse_func
from colors import \
    SOFT_GRAY, RED, GREEN, BLUE, \
    DARK_GRAYISH_BLACK
from color_calc import convert_3pixels_to_3bytes, convert_3bars_to_3bytes
from bar_box import BarBox
from circle_rail import CircleRail
from outer_circle import OuterCircle
from conf import GRID_UNIT, PHASE_COUNTS, FONT_SCALE
from inscribed_triangle import InscribedTriangle
from clock_hand import ClockHand

# 描画する画像を作る
# 横幅 約500 以上にすると ブログで縮小されて .gif ではなくなるので、横幅を 約500未満にすること（＾～＾）
CANVAS_WIDTH = 800  # crieitブログは少なくとも 横幅 450px なら圧縮されない（＾～＾） 470px なら圧縮されてしまう（＾～＾）
CANVAS_HEIGHT = 800
CHANNELS = 3
# モノクロ背景 0黒→255白 178=SOFT_GRAY
MONO_BACKGROUND = SOFT_GRAY[0]

# RGBバー（レールとなる円より上にある）
BAR_BOX_TOP = 6 * GRID_UNIT
# 箱の左
BAR_BOX_LEFT = int(18 * GRID_UNIT)
# 円の中心と、箱の左との距離
CIRCLE_DISTANCE = int(14 * GRID_UNIT)

# とりあえず 11トーン
VERTICAL_PARCENT = [
    # 鮮やかさ2番
    # [0.1, 0.7, 0.2],  # Bright
    # [0.2, 0.7, 0.1],  # Strong
    # [0.3, 0.7, 0.0],  # Deep
    # 鮮やかさ3番
    # [0.0, 0.4, 0.6],  # Light
    # [0.1, 0.4, 0.5],  # Soft
    # [0.3, 0.4, 0.3],  # Dull
    # [0.4, 0.4, 0.2],  # Dark
    # 鮮やかさ4番
    # [0.0, 0.3, 0.7],  # Pale
    # [0.2, 0.3, 0.5],  # Light grayish
    # [0.4, 0.3, 0.3],  # Grayish
    # [0.6, 0.3, 0.1],  # Dark grayish
    # 鮮やかさ1番
    [0.0, 1.0, 0.0],  # Vivid
]
TONE_NAME = [
    # 'Bright',
    # 'Strong',
    # 'Deep',
    # 'Light',
    # 'Soft',
    # 'Dull',
    # 'Dark',
    # 'Pale',
    # 'Light grayish',
    # 'Grayish',
    # 'Dark grayish',
    'Vivid',  # Cosine curve
]


def main():
    """RGB値の仕組みが分かるgifアニメ画像を出力します
    """

    # 連番
    seq = 0

    size = len(VERTICAL_PARCENT)
    for i in range(0, size):
        vertical_parcent = VERTICAL_PARCENT[i]
        tone_name = TONE_NAME[i]

        # 描画：トーン名と バー箱 の紹介
        outer_circle = OuterCircle()
        for _ in range(0, 10):  # Wait frames
            canvas = make_canvas()
            bar_box, circle_rail, _outer_circle, _inscribed_triangle, _clock_hand = update_scene1(
                vertical_parcent, outer_circle)
            draw_grid(canvas)
            circle_rail.draw_circle(canvas)  # 円レール
            circle_rail.draw_border(canvas)  # 背景の上限、下限の線
            bar_box.draw_outline(canvas)
            bar_box.draw_rank2_box(canvas)
            bar_box.draw_bars_rate(canvas)  # バー率テキスト
            draw_tone_name(canvas, bar_box, tone_name)
            # 書出し
            canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)  # BGRをRGBにする
            cv2.imwrite(f"./shared/out-cstep4-{seq}.png", canvas)
            seq += 1

        # 描画：色相環のアニメーション表示
        seq, canvas = update_circle(canvas, seq, vertical_parcent, tone_name)

        for _ in range(0, 10):  # Wait frames
            cv2.imwrite(f"./shared/out-cstep4-{seq}.png", canvas)
            seq += 1


def update_circle(canvas, seq, vertical_parcent, tone_name):
    """色相環一周分の画像を出力"""

    outer_circle = OuterCircle()

    for phase in range(0, PHASE_COUNTS):
        canvas = make_canvas()
        bar_box, circle_rail, outer_circle, inscribed_triangle, clock_hand = update_scene1(
            vertical_parcent, outer_circle)
        update_scene1_with_rotate(vertical_parcent,
                                  phase, bar_box, circle_rail, outer_circle,
                                  inscribed_triangle, clock_hand)

        draw_grid(canvas)  # 罫線
        bar_box.draw_outline(canvas)  # 箱の輪郭
        canvas = draw_canvas(canvas, bar_box, circle_rail,
                             outer_circle, inscribed_triangle, clock_hand)
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


def update_scene1(vertical_parcent, outer_circle):
    """オブジェクトの位置とキャンバスを返します
    """

    # RGBバー
    bar_box = BarBox()
    bar_box.rates = vertical_parcent
    width1 = int(bar_box.rates[0] * 20 * GRID_UNIT)
    width2 = int(bar_box.rates[1] * 20 * GRID_UNIT)
    width3 = int(bar_box.rates[2] * 20 * GRID_UNIT)
    bar_box.left = BAR_BOX_LEFT
    bar_box.lower_x = bar_box.left + width3
    bar_box.upper_x = bar_box.lower_x + width2
    bar_box.right = bar_box.upper_x + width1
    bar_box.top = BAR_BOX_TOP
    bar_box.bottom = bar_box.top + 90
    bar_box.label_gap = int(-0.75*GRID_UNIT)
    bar_box.font_scale = FONT_SCALE
    bar_box.line_type = 2
    bar_box.font = cv2.FONT_HERSHEY_SIMPLEX

    # レールとなる円 circle rail
    circle_rail = CircleRail()
    circle_rail.border_top = bar_box.bottom + GRID_UNIT
    circle_rail.border_bottom = CANVAS_HEIGHT - GRID_UNIT
    circle_rail.range1 = int(width2 / 2)

    circle_rail.center = (int((bar_box.lower_x+bar_box.upper_x)/2),
                          bar_box.bottom+CIRCLE_DISTANCE+circle_rail.range1)  # x, y
    circle_rail.point_range = 4

    outer_circle.origin = (circle_rail.center[0], circle_rail.center[1])
    outer_circle.area_size = (int(bar_box.width*9/10),
                              int(bar_box.width*9/10))
    outer_circle.phases = PHASE_COUNTS

    inscribed_triangle = InscribedTriangle()

    # 時計の針
    clock_hand = ClockHand()
    clock_hand.center = (circle_rail.center[0], circle_rail.center[1])
    clock_hand.unit_arc = outer_circle.unit_arc
    clock_hand.tickness = 2
    clock_hand.rng1 = circle_rail.range1  # 1st range
    clock_hand.rng2 = int(bar_box.width*9/10-GRID_UNIT) - \
        clock_hand.tickness  # 2nd range
    clock_hand.rng3 = int(bar_box.width*9/10)+clock_hand.tickness  # 3rd range

    return bar_box, circle_rail, outer_circle, inscribed_triangle, clock_hand


def update_scene1_with_rotate(
        vertical_parcent, phase, bar_box, circle_rail, outer_circle,
        inscribed_triangle, clock_hand):
    """回転が伴うモデルを更新"""
    theta = 360/PHASE_COUNTS*phase

    outer_circle.phase = phase

    # 円周上の点の位置
    circle_rail.theta = theta

    color_rate = to_color_rate(vertical_parcent, theta)

    # バーの横幅に変換
    red_bar_width = int(color_rate[0] * bar_box.width)
    green_bar_width = int(color_rate[1] * bar_box.width)
    blue_bar_width = int(color_rate[2] * bar_box.width)

    # 逆関数のテスト
    expected_upper = int(
        255 * (bar_box.upper_x - bar_box.left) / bar_box.width)
    expected_lower = int(
        255 * (bar_box.lower_x - bar_box.left) / bar_box.width)
    expected_theta = theta
    expected_color = (int(255*color_rate[0]),
                      int(255*color_rate[1]),
                      int(255*color_rate[2]))
    actual_theta, actual_upper, actual_lower, pattern = inverse_func(
        expected_color)
    # 誤差 +-1 まで許容
    if actual_upper < expected_upper - 1.0 or expected_upper + 1.0 < actual_upper:
        diff = actual_upper - expected_upper
        print(
            f"ERROR           | expected_upper={expected_upper:3} \
actual_upper={actual_upper:3} diff={diff} theta={theta} pattern={pattern}")
    if actual_lower < expected_lower - 1.0 or expected_lower + 1.0 < actual_lower:
        diff = actual_lower - expected_lower
        print(
            f"ERROR           | expected_lower={expected_lower:3} \
actual_lower={actual_lower:3} diff={diff} theta={theta} pattern={pattern}")
    if actual_theta < expected_theta - 1.0 or expected_theta + 1.0 < actual_theta:
        diff = actual_theta - expected_theta
        print(
            f"ERROR           | expected_theta={expected_theta}° \
actual_theta={actual_theta:9.4f}° diff={diff:9.4f} pattern={pattern}")

    # バーR
    bar_box.red_right = bar_box.left + red_bar_width
    # バーG
    bar_box.green_right = bar_box.left + green_bar_width
    # バーB
    bar_box.blue_right = bar_box.left + blue_bar_width

    # 外環状
    theta = outer_circle.phase * outer_circle.unit_arc
    n3bars_width = bar_box.create_3bars_width()
    outer_circle.color_list.append(convert_3pixels_to_3bytes(
        n3bars_width, bar_box.width))
    #

    inscribed_triangle.update(
        bar_box.upper_x, bar_box.lower_x, circle_rail.center, theta, n3bars_width)

    gravity = inscribed_triangle.triangular_center_of_gravity()
    diff_xy = (gravity[0] - circle_rail.center[0],
               gravity[1] - circle_rail.center[1])
    inscribed_triangle.correct_horizon(diff_xy)

    # 時計の針
    clock_hand.theta = theta


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
                (bar_box.left, int(BAR_BOX_TOP-3.5*GRID_UNIT)),  # x,y
                cv2.FONT_HERSHEY_SIMPLEX,
                FONT_SCALE,
                DARK_GRAYISH_BLACK,
                line_type)
    cv2.putText(canvas,
                f"tone diameter",
                (bar_box.left+GRID_UNIT, int(BAR_BOX_TOP-2.5*GRID_UNIT)),  # x,y
                cv2.FONT_HERSHEY_SIMPLEX,
                FONT_SCALE,
                DARK_GRAYISH_BLACK,
                line_type)


def draw_canvas(canvas, bar_box, circle_rail, outer_circle, inscribed_triangle, clock_hand):
    """アニメの１コマを作成します"""

    circle_rail.draw_circle(canvas)  # 円レール
    circle_rail.draw_triangle(canvas)  # 円に内接する正三角形
    circle_rail.draw_border(canvas)  # 背景の上限、下限の線

    inscribed_triangle.draw(canvas)

    bar_box.draw_3bars(canvas)  # RGBバー

    bar_box.draw_x_axis_label(canvas)  # X軸のラベル

    # 水平線R
    # 線、描画する画像を指定、座標1点目、2点目、色、線の太さ
    cv2.line(canvas,
             inscribed_triangle.rbg_points[0],
             (bar_box.red_right, bar_box.red_top),
             RED, thickness=2)

    # 水平線G
    cv2.line(canvas,
             inscribed_triangle.rbg_points[2],  # 青と緑が入れ替わっているのが工夫
             (bar_box.green_right, bar_box.green_top),
             GREEN, thickness=2)

    # 水平線B
    cv2.line(canvas,
             inscribed_triangle.rbg_points[1],
             (bar_box.blue_right, bar_box.blue_top),
             BLUE, thickness=2)

    outer_circle.draw_me(canvas)  # 外環状

    # 時計の針
    clock_hand.draw_clock_hand(canvas)

    # バー箱の２段目の黒枠
    bar_box.draw_rank2_box(canvas)

    # 色成分数
    # 1色成分 (高さから 255 へ丸めるとき、誤差が出る)
    n3bars_width = bar_box.create_3bars_width()
    color = convert_3bars_to_3bytes(n3bars_width, bar_box.width)
    bar_box.draw_rgb_number(canvas, color)

    # gravity = inscribed_triangle.triangular_center_of_gravity()

    # debug
    # cv2.putText(canvas,
    #            f"theta={circle_rail.theta}",
    #            # f"theta={circle_rail.theta} phase={outer_circle.phase} \
    #  gravity=({gravity[0]:5.1f}, {gravity[1]:5.1f})",
    #            (10, 10),  # x,y
    #            cv2.FONT_HERSHEY_SIMPLEX,
    #            FONT_SCALE,
    #            BLACK,
    #            lineType=2)
    # f"multiple=({n3bars_multiple[0]:7.3f}, {n3bars_multiple[1]:7.3f}, {n3bars_multiple[2]:7.3f})",

    # cv2.imshow('Title', canvas)
    # cv2.imwrite('form.jpg',canvas)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return canvas


main()
