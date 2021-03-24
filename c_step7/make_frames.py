"""png画像を複数枚出力します
"""

import math
import cv2
import numpy as np
from color_calc import calc_color
from bar_box import BarBox
from circle_rail import CircleRail
from brush_point import BrushPoint

# 色 BGR
# white = (255, 255, 255)
PALE_GRAY = (235, 235, 235)
LIGHT_GRAY = (200, 200, 200)
BLACK = (16, 16, 16)
RED = (250, 100, 100)
GREEN = (100, 250, 100)
BLUE = (100, 100, 250)

# 描画する画像を作る
# 横幅 約500 以上にすると ブログで縮小されて .gif ではなくなるので、横幅を 約500未満にすること（＾～＾）
CANVAS_WIDTH = 440
CANVAS_HEIGHT = 300
CHANNELS = 3
# モノクロ背景 0黒→255白
MONO_BACKGROUND = 255

# 水平線グリッド
GRID_INTERVAL_H = 10
# RGBバー１段目（レールとなる円より上にある）
BAR_TOP1 = 5 * GRID_INTERVAL_H
# 円レール circle rail left
CRAIL_LEFT = 5 * GRID_INTERVAL_H

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
        bar_rate = BAR_RATES[i]
        tone_name = TONE_NAME[i]

        for _ in range(0, 10):  # Wait frames
            canvas, bar_box, _circle_rail, _brush_point = make_canvas_scene1(
                bar_rate)
            draw_bar_box_rank1(canvas, bar_box)
            draw_bar_box_rank3(canvas, bar_box)
            draw_bar_box_rank2(canvas, bar_box)
            draw_tone_name(canvas, bar_box, tone_name)
            # 書出し
            canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)  # BGRをRGBにする
            cv2.imwrite(f"./shared/out-cstep4-{seq}.png", canvas)
            seq += 1

        seq = make_circle(canvas, seq, bar_rate, tone_name)


def make_circle(canvas, seq, bar_rate, tone_name):
    """一周分の画像を出力
    """

    for i in range(0, FRAME_COUNTS):
        theta = 360/FRAME_COUNTS*i
        canvas, bar_box, circle_rail, brush_point = make_canvas_scene1(
            bar_rate)
        draw_bar_box_rank1(canvas, bar_box)
        canvas = draw_canvas(canvas, bar_box, circle_rail, brush_point,
                             theta, bar_rate)
        draw_bar_box_rank3(canvas, bar_box)
        draw_bar_box_rank2(canvas, bar_box)
        draw_tone_name(canvas, bar_box, tone_name)

        # 書出し
        canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)  # BGRをRGBにする
        cv2.imwrite(f"./shared/out-cstep4-{seq}.png", canvas)
        seq += 1

    return seq


def make_canvas_scene1(bar_rate):
    """アニメの１コマを作成します
    """
    # キャンバス
    canvas = np.full((CANVAS_HEIGHT, CANVAS_WIDTH, CHANNELS),
                     MONO_BACKGROUND, dtype=np.uint8)

    # 水平線グリッド
    for i in range(0, int(CANVAS_HEIGHT/GRID_INTERVAL_H)):
        y_num = GRID_INTERVAL_H*i
        cv2.line(canvas, (0, y_num), (CANVAS_WIDTH, y_num),
                 PALE_GRAY, thickness=1)

    bar_box = BarBox()
    circle_rail = CircleRail()
    brush_point = BrushPoint()
    # バー
    # RGBバーの１段目、２段目、３段目の高さ（２０分率）
    bar_box.height1 = int(bar_rate[0] * 20 * GRID_INTERVAL_H)
    bar_box.height2 = int(bar_rate[1] * 20 * GRID_INTERVAL_H)
    bar_box.height3 = int(bar_rate[2] * 20 * GRID_INTERVAL_H)
    bar_box.one_width = 24
    # 円レール
    circle_rail.range = int(bar_box.height2 / 2)
    # 塗った円
    brush_point.distance = circle_rail.range + 2*GRID_INTERVAL_H
    brush_point.range = GRID_INTERVAL_H
    # バー箱の左
    range_width = 10
    outer_circle_margin = 2
    width = 2 * (range_width + outer_circle_margin)
    bar_box.left = int(CRAIL_LEFT + width*GRID_INTERVAL_H +
                       2*brush_point.range)
    # バーの筋
    bar_box.red_left = bar_box.left
    bar_box.green_left = bar_box.red_left + bar_box.one_width + 1
    bar_box.blue_left = bar_box.green_left + bar_box.one_width + 1
    bar_box.right = bar_box.blue_left + bar_box.one_width
    # レールとなる円 circle rail
    circle_rail.top = BAR_TOP1 + bar_box.height1
    circle_rail.center = (CRAIL_LEFT+circle_rail.range,
                          circle_rail.top+circle_rail.range)  # x, y
    circle_rail.point_range = 6
    # RGBバー２段目
    bar_box.top2 = circle_rail.top
    bar_box.rank1_p1 = (bar_box.left, BAR_TOP1)
    bar_box.rank1_p2 = (bar_box.right, bar_box.top2)
    # バー２段目（レールとなる円と水平線を合わす）
    bar_box.top3 = bar_box.top2 + bar_box.height2
    bar_box.bottom = bar_box.top3 + bar_box.height3
    bar_box.height = bar_box.height1 + bar_box.height2 + bar_box.height3
    # RGBバー(中部)領域
    bar_box.rank2_p1 = (bar_box.left, bar_box.top2)
    bar_box.rank2_p2 = (bar_box.right, bar_box.top3)
    # RGBバー３段目
    bar_box.rank3_p1 = (bar_box.left, bar_box.top3)
    bar_box.rank3_p2 = (bar_box.right, bar_box.bottom)

    return canvas, bar_box, circle_rail, brush_point


def draw_bar_box_rank1(canvas, bar_box):
    """バー箱の１段目の箱を描きます"""
    cv2.rectangle(canvas, bar_box.rank1_p1,
                  bar_box.rank1_p2, LIGHT_GRAY, thickness=4)


def draw_bar_box_rank2(canvas, bar_box):
    """バー箱の２段目の箱を描きます"""
    cv2.rectangle(canvas, bar_box.rank2_p1,
                  bar_box.rank2_p2, BLACK, thickness=4)


def draw_bar_box_rank3(canvas, bar_box):
    """バー箱の３段目の箱を描きます"""
    cv2.rectangle(canvas, bar_box.rank3_p1,
                  bar_box.rank3_p2, LIGHT_GRAY, thickness=4)


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


def draw_canvas(canvas, bar_box, circle_rail, brush_point, base_theta, bar_rate):
    """アニメの１コマを作成します
    """

    # 円レール。描画する画像を指定、座標（x,y),半径、色、線の太さ（-1は塗りつぶし）
    cv2.circle(canvas, circle_rail.center,
               circle_rail.range, LIGHT_GRAY, thickness=2)

    # 円周上の点の位置
    theta = base_theta % 360
    red_p = circle_rail.calc_red_p(theta)
    green_p = circle_rail.calc_green_p(theta)
    blue_p = circle_rail.calc_blue_p(theta)

    # バーR
    bar_box.red_bar_p1 = (bar_box.red_left, red_p[1])
    bar_box.red_bar_p2 = (bar_box.red_left+bar_box.one_width, bar_box.bottom)
    # バーG
    bar_box.green_bar_p1 = (bar_box.green_left, green_p[1])
    bar_box.green_bar_p2 = (
        bar_box.green_left+bar_box.one_width, bar_box.bottom)
    # バーB
    bar_box.blue_bar_p1 = (bar_box.blue_left, blue_p[1])
    bar_box.blue_bar_p2 = (bar_box.blue_left+bar_box.one_width, bar_box.bottom)

    # 点R
    cv2.circle(canvas, red_p, circle_rail.point_range, RED, thickness=-1)

    # 点G
    cv2.circle(canvas, green_p, circle_rail.point_range, GREEN, thickness=-1)

    # 点B
    cv2.circle(canvas, blue_p, circle_rail.point_range, BLUE, thickness=-1)

    # 円に内接する線。三角形
    cv2.line(canvas, (red_p[0], red_p[1]),
             (green_p[0], green_p[1]), BLACK, thickness=2)
    cv2.line(canvas, (green_p[0], green_p[1]),
             (blue_p[0], blue_p[1]), BLACK, thickness=2)
    cv2.line(canvas, (blue_p[0], blue_p[1]),
             (red_p[0], red_p[1]), BLACK, thickness=2)

    # 水平線R
    # 線、描画する画像を指定、座標1点目、2点目、色、線の太さ
    cv2.line(canvas, (red_p[0], red_p[1]),
             (bar_box.red_left, red_p[1]), RED, thickness=2)

    # 水平線G
    cv2.line(canvas, (green_p[0], green_p[1]),
             (bar_box.green_left, green_p[1]), GREEN, thickness=2)

    # 水平線B
    cv2.line(canvas, (blue_p[0], blue_p[1]),
             (bar_box.blue_left, blue_p[1]), BLUE, thickness=2)

    # バーR
    cv2.rectangle(canvas, bar_box.red_bar_p1,
                  bar_box.red_bar_p2, RED, thickness=-1)

    # バーG
    cv2.rectangle(canvas, bar_box.green_bar_p1,
                  bar_box.green_bar_p2, GREEN, thickness=-1)

    # バーB
    cv2.rectangle(canvas, bar_box.blue_bar_p1,
                  bar_box.blue_bar_p2, BLUE, thickness=-1)

    # 色値
    valurr = 255-int((red_p[1]-BAR_TOP1)/bar_box.height*255)
    valurg = 255-int((green_p[1]-BAR_TOP1)/bar_box.height*255)
    valurb = 255-int((blue_p[1]-BAR_TOP1)/bar_box.height*255)

    # R値テキスト
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_height = 20
    font_scale = 0.6
    line_type = 2
    cv2.putText(canvas,
                f"{valurr:02x}",
                (bar_box.red_bar_p2[0]-bar_box.one_width,
                 bar_box.red_bar_p2[1]+font_height),  # x,y
                font,
                font_scale,
                RED,
                line_type)

    # G値テキスト
    cv2.putText(canvas,
                f"{valurg:02x}",
                (bar_box.green_bar_p2[0]-bar_box.one_width,
                 bar_box.green_bar_p2[1]+font_height),  # x,y
                font,
                font_scale,
                GREEN,
                line_type)

    # B値テキスト
    cv2.putText(canvas,
                f"{valurb:02x}",
                (bar_box.blue_bar_p2[0]-bar_box.one_width,
                 bar_box.blue_bar_p2[1]+font_height),  # x,y
                font,
                font_scale,
                BLUE,
                line_type)

    # バー率
    rate_y = int((BAR_TOP1 + bar_box.top2)/2)
    cv2.putText(canvas,
                f"{bar_rate[0]}",
                (bar_box.right+bar_box.one_width, rate_y),  # x,y
                font,
                font_scale,
                LIGHT_GRAY,
                line_type)
    rate_y = int((bar_box.top2 + bar_box.top3)/2)
    cv2.putText(canvas,
                f"{bar_rate[1]}",
                (bar_box.right+bar_box.one_width, rate_y),  # x,y
                font,
                font_scale,
                BLACK,
                line_type)
    rate_y = int((bar_box.top3 + bar_box.bottom)/2)
    cv2.putText(canvas,
                f"{bar_rate[2]}",
                (bar_box.right+bar_box.one_width, rate_y),  # x,y
                font,
                font_scale,
                LIGHT_GRAY,
                line_type)

    # 色円
    color = (valurr, valurg, valurb)
    # print(f"({red_p[1]},{green_p[1]},{blue_p[1]})")
    # var1 = int(red_p[1]/bar_max_height*255)
    # var2 = int(green_p[1]/bar_max_height*255)
    # var3 = int(blue_p[1]/bar_max_height*255)
    # print(
    #    f"color={color} ({var1},{var2},{var3})")
    # print(
    #    f"color={color} ({red_p[1]},{green_p[1]},{blue_p[1]}) bar_max_height={bar_max_height}")
    theta2 = base_theta
    red_p = (int(brush_point.distance * math.sin(math.radians(theta2)) + circle_rail.center[0]),
             int(-brush_point.distance * math.cos(math.radians(theta2)) + circle_rail.center[1]))  # yは上下反転
    cv2.circle(canvas, red_p, brush_point.range, color, thickness=-1)

    # 外環状
    outer_circle(canvas, brush_point.distance, circle_rail.center, bar_rate)

    # cv2.imshow('Title', canvas)
    # cv2.imwrite('form.jpg',canvas)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return canvas


def outer_circle(canvas, color_pallete_range, center, bar_rate):
    """外環状
    """

    size = 18
    circumference = 360  # 半径１の円の一周の長さ
    unit_arc = circumference/size  # 等分割した１つの弧

    color_list = []
    for i in range(0, size):
        theta = i * unit_arc
        color = calc_color(theta, bar_rate)
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
