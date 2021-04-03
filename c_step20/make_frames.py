"""png画像を複数枚出力します
"""

import math
import cv2
import numpy as np
from color_hul_model import to_color_rate
from colors import PALE_GRAY,  \
    SOFT_GRAY, RED, GREEN, BLUE, \
    DARK_GRAYISH_BLACK
from color_calc import convert_3heights_to_3bytes
from bar_box import BarBox
from circle_rail import CircleRail
from outer_circle import OuterCircle
from conf import GRID_UNIT, PHASE_COUNTS, FONT_SCALE
from inscribed_triangle import InscribedTriangle
from rectangle import Rectangle

# 描画する画像を作る
# 横幅 約500 以上にすると ブログで縮小されて .gif ではなくなるので、横幅を 約500未満にすること（＾～＾）
CANVAS_WIDTH = 450  # crieitブログは少なくとも 横幅 450px なら圧縮されない（＾～＾） 470px なら圧縮されてしまう（＾～＾）
CANVAS_HEIGHT = 400
CHANNELS = 3
# モノクロ背景 0黒→255白 178=SOFT_GRAY
MONO_BACKGROUND = SOFT_GRAY[0]

# RGBバー１段目（レールとなる円より上にある）
BAR_TOP1 = 9 * GRID_UNIT
# 箱の左
BAR_BOX_LEFT = int(22 * GRID_UNIT)
# 円の中心と、箱の左との距離
CIRCLE_DISTANCE = int(11.5 * GRID_UNIT)

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
    [0.4, 0.3, 0.3],  # Grayish
    # [0.6, 0.3, 0.1],  # Dark grayish
    # 鮮やかさ1番
    # [0.0, 1.0, 0.0],  # Vivid
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
    'Grayish',
    # 'Dark grayish',
    # 'Vivid',  # Cosine curve
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
            bar_box, circle_rail, _outer_circle, _inscribed_triangle = update_scene1(
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
        bar_box, circle_rail, outer_circle, inscribed_triangle = update_scene1(
            vertical_parcent, outer_circle)
        update_scene1_with_rotate(vertical_parcent,
                                  phase, bar_box, circle_rail, outer_circle, inscribed_triangle)

        draw_grid(canvas)  # 罫線
        bar_box.draw_outline(canvas)  # 箱の輪郭
        canvas = draw_canvas(canvas, bar_box, circle_rail,
                             outer_circle, inscribed_triangle)
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

    bar_box = BarBox()
    circle_rail = CircleRail()
    inscribed_triangle = InscribedTriangle()

    # バー
    # RGBバーの１段目、２段目、３段目の高さ（２０分率）
    bar_box.top1 = BAR_TOP1
    bar_box.rates = vertical_parcent
    bar_box.height1 = int(bar_box.rates[0] * 10 * GRID_UNIT)
    bar_box.height2 = int(bar_box.rates[1] * 10 * GRID_UNIT)
    bar_box.height3 = int(bar_box.rates[2] * 10 * GRID_UNIT)
    bar_box.one_width = 30  # フォント１文字の横幅が 10 と想定
    bar_box.y_axis_label_gap = int(0.25*GRID_UNIT)
    bar_box.rate_text_gap = int(0.2*GRID_UNIT)

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

    # 円レール
    circle_rail.range1 = int(bar_box.height2 / 2)
    circle_rail.border_left = GRID_UNIT
    circle_rail.border_right = bar_box.left - GRID_UNIT

    circle_rail.center = (bar_box.left - CIRCLE_DISTANCE,
                          circle_rail.top+circle_rail.range1)  # x, y
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

    return bar_box, circle_rail, outer_circle, inscribed_triangle


def update_scene1_with_rotate(
        vertical_parcent, phase, bar_box, circle_rail, outer_circle, inscribed_triangle):
    """回転が伴うモデルを更新"""
    theta = 360/PHASE_COUNTS*phase

    outer_circle.phase = phase

    # 円周上の点の位置
    circle_rail.theta = theta

#    print(
#        f"vertical_parcent=({vertical_parcent[0]}, {vertical_parcent[1]}, \
# {vertical_parcent[2]}) theta={theta}")
    color_rate = to_color_rate(vertical_parcent, theta)
#    print(
#        f"color_rate=({color_rate[0]}, {color_rate[1]}, {color_rate[2]})")

    # バーの高さに変換
    red_bar_height = int(color_rate[0] * bar_box.height)
    green_bar_height = int(color_rate[1] * bar_box.height)
    blue_bar_height = int(color_rate[2] * bar_box.height)
#    print(
#        f"red_bar_height={red_bar_height} green_bar_height={green_bar_height} \
# blue_bar_height={blue_bar_height}")

    # バーR ( (left, top), (right, bottom) )
    # バーG
    # バーB
    bar_box.n3bars_rect = (
        Rectangle(
            bar_box.red_left,
            bar_box.bottom - red_bar_height,
            bar_box.red_left+bar_box.one_width,
            bar_box.top3),
        Rectangle(
            bar_box.green_left,
            bar_box.bottom - green_bar_height,
            bar_box.green_left+bar_box.one_width,
            bar_box.top3),
        Rectangle(
            bar_box.blue_left,
            bar_box.bottom - blue_bar_height,
            bar_box.blue_left+bar_box.one_width,
            bar_box.top3))

    # 外環状
    theta = outer_circle.phase * outer_circle.unit_arc
    rank23d_3bars_height = bar_box.create_rank23d_3bars_height()
    outer_circle.color_list.append(convert_3heights_to_3bytes(
        rank23d_3bars_height, bar_box.height))
    #

    inscribed_triangle.update(
        bar_box.top2, bar_box.top3, circle_rail.center, theta, rank23d_3bars_height)

    gravity = inscribed_triangle.triangular_center_of_gravity()
    diff_xy = (gravity[0] - circle_rail.center[0],
               gravity[1] - circle_rail.center[1])
    inscribed_triangle.correct_horizon(diff_xy)


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
                (bar_box.left, int(BAR_TOP1-3.5*GRID_UNIT)),  # x,y
                cv2.FONT_HERSHEY_SIMPLEX,
                FONT_SCALE,
                DARK_GRAYISH_BLACK,
                line_type)
    cv2.putText(canvas,
                f"tone diameter",
                (bar_box.left+GRID_UNIT, int(BAR_TOP1-2.5*GRID_UNIT)),  # x,y
                cv2.FONT_HERSHEY_SIMPLEX,
                FONT_SCALE,
                DARK_GRAYISH_BLACK,
                line_type)


def draw_canvas(canvas, bar_box, circle_rail, outer_circle, inscribed_triangle):
    """アニメの１コマを作成します"""

    circle_rail.draw_circle(canvas)  # 円レール
    circle_rail.draw_triangle(canvas)  # 円に内接する正三角形
    circle_rail.draw_border(canvas)  # 背景の上限、下限の線

    inscribed_triangle.draw(canvas)

    # 1色成分 (高さから 255 へ丸めるとき、誤差が出る)
    rank23d_3bars_height = bar_box.create_rank23d_3bars_height()
    rank23d_color = convert_3heights_to_3bytes(
        rank23d_3bars_height, bar_box.height)
    bar_box.draw_3bars(canvas)  # RGBバー

    bar_box.draw_y_axis_label(canvas)  # バー率テキスト

    # 水平線R
    # 線、描画する画像を指定、座標1点目、2点目、色、線の太さ
    cv2.line(canvas,
             inscribed_triangle.rbg_points[0],
             (bar_box.red_left, bar_box.red_top),
             RED, thickness=2)

    # 水平線G
    cv2.line(canvas,
             inscribed_triangle.rbg_points[2],  # 青と緑が入れ替わっているのが工夫
             (bar_box.green_left, bar_box.green_top),
             GREEN, thickness=2)

    # 水平線B
    cv2.line(canvas,
             inscribed_triangle.rbg_points[1],
             (bar_box.blue_left, bar_box.blue_top),
             BLUE, thickness=2)

    outer_circle.draw_me(canvas)  # 外環状

    # 時計の針
    tickness = 2
    inner_range = circle_rail.range1
    second_range = int(6.5*GRID_UNIT)-tickness
    third_range = int(7.5*GRID_UNIT)+tickness
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
    # 時計の針の先
    # 楕円、描画する画像を指定、座標(x,y),xyの半径、角度,色、線の太さ(-1は塗りつぶし)
    start_angle = int(circle_rail.theta-outer_circle.unit_arc/2)
    end_angle = int(circle_rail.theta+outer_circle.unit_arc/2)
    if start_angle == end_angle:
        end_angle += 1  # 差が 0 だと変なとこ描画するんで
    cv2.ellipse(canvas,
                circle_rail.center,
                (second_range, second_range),
                -90,
                start_angle,
                end_angle,
                PALE_GRAY,
                thickness=tickness)
    cv2.ellipse(canvas,
                circle_rail.center,
                (third_range, third_range),
                -90,
                start_angle,
                end_angle,
                PALE_GRAY,
                thickness=tickness)
    #

    # バー箱の２段目の黒枠
    bar_box.draw_rank2_box(canvas)

    # 色成分数
    bar_box.draw_rgb_number(canvas,
                            rank23d_color)

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
