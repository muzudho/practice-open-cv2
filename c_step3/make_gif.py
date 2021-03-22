import cv2
import numpy as np
from PIL import Image
from datetime import datetime
import math


def main():
    """RGB値の仕組みが分かるgifアニメ画像を出力します
    """
    images = []

    for i in range(0, 36):
        theta = 10*i
        image = make_frame(theta)
        images.append(image)

    # cv2.imshow('canvas',canvas)
    # cv2.imwrite('form.jpg',canvas)
    date = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = f"out-{date}.gif"
    fps = 4
    duration_time = int(1000.0 / fps)
    images[0].save(path,
                   save_all=True,
                   append_images=images[1:],
                   optimize=False,
                   duration=duration_time,
                   loop=0)


def make_frame(base_theta):
    """アニメの１コマを作成します
    """
    # 色 BGR
    # white = (255, 255, 255)
    pale_gray = (235, 235, 235)
    light_gray = (200, 200, 200)
    black = (16, 16, 16)
    red = (250, 100, 100)
    green = (100, 250, 100)
    blue = (100, 100, 250)

    # 描画する画像を作る
    # 横幅 約500 以上にすると ブログで縮小されて .gif ではなくなるので、横幅を 約500未満にすること（＾～＾）
    canvas_width = 512
    canvas_height = 384
    channels = 3
    # 0黒→255白
    background = 255

    # キャンバス
    canvas = np.full((canvas_height, canvas_width, channels),
                     background, dtype=np.uint8)

    # 水平線グリッド
    grid_interval_h = 16
    for i in range(0, int(canvas_height/grid_interval_h)):
        y = grid_interval_h*i
        cv2.line(canvas, (0, y), (canvas_width, y), pale_gray, thickness=1)

    # バーの筋
    bar_left = 300
    bar_width = 24
    barr_x = bar_left
    barg_x = 325
    barb_x = 350
    bar_right = barb_x + bar_width

    # RGBバーの１段目の高さ
    bar_box_height1 = 4 * grid_interval_h

    # RGBバー１段目（レールとなる円より上にある）
    bar_top1 = 1 * grid_interval_h

    # レールとなる円
    circle_rail_top = bar_top1 + bar_box_height1
    circle_rail_left = 3 * grid_interval_h
    circle_rail_range = 5 * grid_interval_h
    circle_rail_center = (circle_rail_left+circle_rail_range,
                          circle_rail_top+circle_rail_range)  # x, y

    # RGBバー２段目
    bar_top2 = circle_rail_top
    bar_area1_p1 = (bar_left, bar_top1)
    bar_area1_p2 = (bar_right, bar_top2)

    # 色円
    color_pallete_range = circle_rail_range + 2*grid_interval_h
    color_pallete_circle_range = grid_interval_h

    # バー２段目（レールとなる円と水平線を合わす）
    bar_box_height2 = 2*circle_rail_range
    bar_top3 = bar_top2 + bar_box_height2
    bar_box_height3 = 0
    bar_bottom = bar_top3 + bar_box_height3
    bar_box_height = bar_box_height1 + bar_box_height2 + bar_box_height3

    # 円、描画する画像を指定、座標（x,y),半径、色、線の太さ（-1は塗りつぶし）
    cv2.circle(canvas, circle_rail_center,
               circle_rail_range, black, thickness=2)

    # 点R
    point_range = 6
    theta = (0+base_theta) % 360
    pr = (int(circle_rail_range * math.sin(math.radians(theta)) + circle_rail_center[0]),
          int(-circle_rail_range * math.cos(math.radians(theta)) + circle_rail_center[1]))  # yは上下反転
    cv2.circle(canvas, pr, point_range, red, thickness=-1)

    # 点G
    theta = (240+base_theta) % 360  # 時計回り
    pg = (int(circle_rail_range * math.sin(math.radians(theta)) + circle_rail_center[0]),
          int(-circle_rail_range * math.cos(math.radians(theta)) + circle_rail_center[1]))  # yは上下反転
    cv2.circle(canvas, pg, point_range, green, thickness=-1)

    # 点B
    theta = (120+base_theta) % 360
    pb = (int(circle_rail_range * math.sin(math.radians(theta)) + circle_rail_center[0]),
          int(-circle_rail_range * math.cos(math.radians(theta)) + circle_rail_center[1]))  # yは上下反転
    cv2.circle(canvas, pb, point_range, blue, thickness=-1)

    # 水平線R
    # 線、描画する画像を指定、座標1点目、2点目、色、線の太さ
    cv2.line(canvas, (pr[0], pr[1]), (barr_x, pr[1]), red, thickness=2)

    # 水平線G
    cv2.line(canvas, (pg[0], pg[1]), (barg_x, pg[1]), green, thickness=2)

    # 水平線B
    cv2.line(canvas, (pb[0], pb[1]), (barb_x, pb[1]), blue, thickness=2)

    cv2.rectangle(canvas, bar_area1_p1, bar_area1_p2, light_gray, thickness=4)

    # RGBバー(中部)領域
    bar_area2_p1 = (bar_left, bar_top2)
    bar_area2_p2 = (bar_right, bar_bottom)
    cv2.rectangle(canvas, bar_area2_p1, bar_area2_p2, light_gray, thickness=4)

    # バーR
    barr_p1 = (barr_x, pr[1])
    barr_p2 = (barr_x+bar_width, bar_bottom)
    cv2.rectangle(canvas, barr_p1, barr_p2, red, thickness=-1)

    # バーG
    barg_p1 = (barg_x, pg[1])
    barg_p2 = (barg_x+bar_width, bar_bottom)
    cv2.rectangle(canvas, barg_p1, barg_p2, green, thickness=-1)

    # バーB
    barb_p1 = (barb_x, pb[1])
    barb_p2 = (barb_x+bar_width, bar_bottom)
    cv2.rectangle(canvas, barb_p1, barb_p2, blue, thickness=-1)

    # 色値
    valurr = 255-int((pr[1]-bar_top1)/bar_box_height*255)
    valurg = 255-int((pg[1]-bar_top1)/bar_box_height*255)
    valurb = 255-int((pb[1]-bar_top1)/bar_box_height*255)

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
                red,
                line_type)

    # G値テキスト
    cv2.putText(canvas,
                f"{valurg:02x}",
                (barg_p2[0]-bar_width, barg_p2[1]+font_height),  # x,y
                font,
                font_scale,
                green,
                line_type)

    # B値テキスト
    cv2.putText(canvas,
                f"{valurb:02x}",
                (barb_p2[0]-bar_width, barb_p2[1]+font_height),  # x,y
                font,
                font_scale,
                blue,
                line_type)

    # 色円
    color = (valurr, valurg, valurb)
    # print(f"({pr[1]},{pg[1]},{pb[1]})")
    # print(f"({pr[1]-bar_top},{pg[1]-bar_top},{pb[1]-bar_top})")
    # print(
    #    f"color={color} ({int(pr[1]/bar_max_height*255)},{int(pg[1]/bar_max_height*255)},{int(pb[1]/bar_max_height*255)})")
    # print(
    #    f"color={color} ({pr[1]},{pg[1]},{pb[1]}) bar_max_height={bar_max_height}")
    theta2 = base_theta
    pr = (int(color_pallete_range * math.sin(math.radians(theta2)) + circle_rail_center[0]),
          int(-color_pallete_range * math.cos(math.radians(theta2)) + circle_rail_center[1]))  # yは上下反転
    cv2.circle(canvas, pr, color_pallete_circle_range, color, thickness=-1)

    return Image.fromarray(canvas)


main()
