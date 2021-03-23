"""png画像を複数枚出力します
"""

import math
import cv2
import numpy as np

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
CANVAS_WIDTH = 560
CANVAS_HEIGHT = 416
CHANNELS = 3
# モノクロ背景 0黒→255白
MONO_BACKGROUND = 255

# バーの筋
BAR_LEFT = 420

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
        seq = make_circle(seq, BAR_RATES[i], TONE_NAME[i])


def make_circle(seq, bar_rate, tone_name):
    """一周分の画像を出力
    """

    for i in range(0, FRAME_COUNTS):
        theta = 360/FRAME_COUNTS*i
        canvas = make_canvas(theta, bar_rate, tone_name)
        # BGRをRGBにする
        canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)

        cv2.imwrite(f"./shared/out-cstep4-{seq}.png", canvas)
        seq += 1

    return seq


def make_canvas(base_theta, bar_rate, tone_name):
    """アニメの１コマを作成します
    """

    # キャンバス
    canvas = np.full((CANVAS_HEIGHT, CANVAS_WIDTH, CHANNELS),
                     MONO_BACKGROUND, dtype=np.uint8)

    # 水平線グリッド
    grid_interval_h = 16
    for i in range(0, int(CANVAS_HEIGHT/grid_interval_h)):
        y_num = grid_interval_h*i
        cv2.line(canvas, (0, y_num), (CANVAS_WIDTH, y_num),
                 PALE_GRAY, thickness=1)

    # バーの筋
    bar_width = 24
    barr_x = BAR_LEFT
    barg_x = barr_x + bar_width + 1
    barb_x = barg_x + bar_width + 1
    bar_right = barb_x + bar_width

    # RGBバー１段目（レールとなる円より上にある）
    bar_top1 = 3 * grid_interval_h

    # RGBバーの１段目、２段目、３段目の高さ（２０分率）
    bar_box_height1 = int(bar_rate[0] * 20 * grid_interval_h)
    bar_box_height2 = int(bar_rate[1] * 20 * grid_interval_h)
    bar_box_height3 = int(bar_rate[2] * 20 * grid_interval_h)

    # レールとなる円 circle rail
    crail_top = bar_top1 + bar_box_height1
    crail_left = 3 * grid_interval_h
    crail_range = int(bar_box_height2 / 2)
    crail_center = (crail_left+crail_range,
                    crail_top+crail_range)  # x, y

    # RGBバー２段目
    bar_top2 = crail_top
    bar_area1_p1 = (BAR_LEFT, bar_top1)
    bar_area1_p2 = (bar_right, bar_top2)

    # 色円
    color_pallete_range = crail_range + 2*grid_interval_h
    color_pallete_circle_range = grid_interval_h

    # バー２段目（レールとなる円と水平線を合わす）
    bar_top3 = bar_top2 + bar_box_height2
    bar_bottom = bar_top3 + bar_box_height3
    bar_box_height = bar_box_height1 + bar_box_height2 + bar_box_height3

    # 円、描画する画像を指定、座標（x,y),半径、色、線の太さ（-1は塗りつぶし）
    cv2.circle(canvas, crail_center,
               crail_range, BLACK, thickness=2)

    # 点R
    point_range = 6
    theta = (0+base_theta) % 360
    red_p = (int(crail_range * math.sin(math.radians(theta)) + crail_center[0]),
             int(-crail_range * math.cos(math.radians(theta)) + crail_center[1]))  # yは上下反転
    cv2.circle(canvas, red_p, point_range, RED, thickness=-1)

    # 点G
    theta = (240+base_theta) % 360  # 時計回り
    green_p = (int(crail_range * math.sin(math.radians(theta)) + crail_center[0]),
               int(-crail_range * math.cos(math.radians(theta)) + crail_center[1]))  # yは上下反転
    cv2.circle(canvas, green_p, point_range, GREEN, thickness=-1)

    # 点B
    theta = (120+base_theta) % 360
    blue_p = (int(crail_range * math.sin(math.radians(theta)) + crail_center[0]),
              int(-crail_range * math.cos(math.radians(theta)) + crail_center[1]))  # yは上下反転
    cv2.circle(canvas, blue_p, point_range, BLUE, thickness=-1)

    # 水平線R
    # 線、描画する画像を指定、座標1点目、2点目、色、線の太さ
    cv2.line(canvas, (red_p[0], red_p[1]),
             (barr_x, red_p[1]), RED, thickness=2)

    # 水平線G
    cv2.line(canvas, (green_p[0], green_p[1]),
             (barg_x, green_p[1]), GREEN, thickness=2)

    # 水平線B
    cv2.line(canvas, (blue_p[0], blue_p[1]),
             (barb_x, blue_p[1]), BLUE, thickness=2)

    cv2.rectangle(canvas, bar_area1_p1, bar_area1_p2, LIGHT_GRAY, thickness=4)

    # RGBバー(中部)領域
    bar_area2_p1 = (BAR_LEFT, bar_top2)
    bar_area2_p2 = (bar_right, bar_bottom)
    cv2.rectangle(canvas, bar_area2_p1, bar_area2_p2, LIGHT_GRAY, thickness=4)

    # バーR
    barr_p1 = (barr_x, red_p[1])
    barr_p2 = (barr_x+bar_width, bar_bottom)
    cv2.rectangle(canvas, barr_p1, barr_p2, RED, thickness=-1)

    # バーG
    barg_p1 = (barg_x, green_p[1])
    barg_p2 = (barg_x+bar_width, bar_bottom)
    cv2.rectangle(canvas, barg_p1, barg_p2, GREEN, thickness=-1)

    # バーB
    barb_p1 = (barb_x, blue_p[1])
    barb_p2 = (barb_x+bar_width, bar_bottom)
    cv2.rectangle(canvas, barb_p1, barb_p2, BLUE, thickness=-1)

    # RGBバー３段目
    bar_area3_p1 = (BAR_LEFT, bar_top3)
    bar_area3_p2 = (bar_right, bar_bottom)
    cv2.rectangle(canvas, bar_area3_p1, bar_area3_p2, LIGHT_GRAY, thickness=4)

    # 色値
    valurr = 255-int((red_p[1]-bar_top1)/bar_box_height*255)
    valurg = 255-int((green_p[1]-bar_top1)/bar_box_height*255)
    valurb = 255-int((blue_p[1]-bar_top1)/bar_box_height*255)

    # R値テキスト
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_height = 20
    font_scale = 0.6
    line_type = 2
    cv2.putText(canvas,
                f"{valurr:02x}",
                (barr_p2[0]-bar_width, barr_p2[1]+font_height),  # x,y
                font,
                font_scale,
                RED,
                line_type)

    # G値テキスト
    cv2.putText(canvas,
                f"{valurg:02x}",
                (barg_p2[0]-bar_width, barg_p2[1]+font_height),  # x,y
                font,
                font_scale,
                GREEN,
                line_type)

    # B値テキスト
    cv2.putText(canvas,
                f"{valurb:02x}",
                (barb_p2[0]-bar_width, barb_p2[1]+font_height),  # x,y
                font,
                font_scale,
                BLUE,
                line_type)

    # バー率
    rate_y = int((bar_top1 + bar_top2)/2)
    cv2.putText(canvas,
                f"{bar_rate[0]}",
                (bar_right+bar_width, rate_y),  # x,y
                font,
                font_scale,
                LIGHT_GRAY,
                line_type)
    rate_y = int((bar_top2 + bar_top3)/2)
    cv2.putText(canvas,
                f"{bar_rate[1]}",
                (bar_right+bar_width, rate_y),  # x,y
                font,
                font_scale,
                BLACK,
                line_type)
    rate_y = int((bar_top3 + bar_bottom)/2)
    cv2.putText(canvas,
                f"{bar_rate[2]}",
                (bar_right+bar_width, rate_y),  # x,y
                font,
                font_scale,
                LIGHT_GRAY,
                line_type)

    # トーン名
    cv2.putText(canvas,
                f"{tone_name}",
                (BAR_LEFT, bar_top1-font_height),  # x,y
                font,
                font_scale,
                BLACK,
                line_type)

    # 色円
    color = (valurr, valurg, valurb)
    # print(f"({red_p[1]},{green_p[1]},{blue_p[1]})")
    # print(f"({red_p[1]-bar_top},{green_p[1]-bar_top},{blue_p[1]-bar_top})")
    # var1 = int(red_p[1]/bar_max_height*255)
    # var2 = int(green_p[1]/bar_max_height*255)
    # var3 = int(blue_p[1]/bar_max_height*255)
    # print(
    #    f"color={color} ({var1},{var2},{var3})")
    # print(
    #    f"color={color} ({red_p[1]},{green_p[1]},{blue_p[1]}) bar_max_height={bar_max_height}")
    theta2 = base_theta
    red_p = (int(color_pallete_range * math.sin(math.radians(theta2)) + crail_center[0]),
             int(-color_pallete_range * math.cos(math.radians(theta2)) + crail_center[1]))  # yは上下反転
    cv2.circle(canvas, red_p, color_pallete_circle_range, color, thickness=-1)

    # cv2.imshow('Title', canvas)
    # cv2.imwrite('form.jpg',canvas)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return canvas


main()
