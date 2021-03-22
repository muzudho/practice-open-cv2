import cv2
import numpy as np
from PIL import Image
from datetime import datetime
import math


def make_gif(base_theta):
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

    circle_center = (140, 140)  # x, y
    circle_range = 90
    color_pallete_range = 120
    color_pallete_circle_range = 20

    bar_top1 = circle_center[1] - circle_range
    bar_box_height1 = 0
    bar_top2 = bar_top1 + bar_box_height1
    bar_box_height2 = 2*circle_range
    bar_top3 = bar_top2 + bar_box_height2
    bar_box_height3 = 0
    bar_bottom = bar_top3 + bar_box_height3
    bar_box_height = bar_box_height1 + bar_box_height2 + bar_box_height3

    # 水平線グリッド
    grid_interval = 16
    for i in range(0, int(canvas_height/grid_interval)):
        y = grid_interval*i
        cv2.line(canvas, (0, y), (canvas_width, y), pale_gray, thickness=1)

    # 円、描画する画像を指定、座標（x,y),半径、色、線の太さ（-1は塗りつぶし）
    cv2.circle(canvas, circle_center, circle_range, black, thickness=2)

    # 点R
    point_range = 6
    theta = (0+base_theta) % 360
    pr = (int(circle_range * math.sin(math.radians(theta)) + circle_center[0]),
          int(-circle_range * math.cos(math.radians(theta)) + circle_center[1]))  # yは上下反転
    cv2.circle(canvas, pr, point_range, red, thickness=-1)

    # 点G
    theta = (240+base_theta) % 360  # 時計回り
    pg = (int(circle_range * math.sin(math.radians(theta)) + circle_center[0]),
          int(-circle_range * math.cos(math.radians(theta)) + circle_center[1]))  # yは上下反転
    cv2.circle(canvas, pg, point_range, green, thickness=-1)

    # 点B
    theta = (120+base_theta) % 360
    pb = (int(circle_range * math.sin(math.radians(theta)) + circle_center[0]),
          int(-circle_range * math.cos(math.radians(theta)) + circle_center[1]))  # yは上下反転
    cv2.circle(canvas, pb, point_range, blue, thickness=-1)

    # バーの筋
    bar_width = 24
    barr_x = 300
    barg_x = 325
    barb_x = 350

    # 水平線R
    # 線、描画する画像を指定、座標1点目、2点目、色、線の太さ
    cv2.line(canvas, (pr[0], pr[1]), (barr_x, pr[1]), red, thickness=2)

    # 水平線G
    cv2.line(canvas, (pg[0], pg[1]), (barg_x, pg[1]), green, thickness=2)

    # 水平線B
    cv2.line(canvas, (pb[0], pb[1]), (barb_x, pb[1]), blue, thickness=2)

    # RGBバー(中部)領域
    bar_area_p1 = (barr_x, bar_top2)
    bar_area_p2 = (barb_x+bar_width, bar_bottom)
    cv2.rectangle(canvas, bar_area_p1, bar_area_p2, light_gray, thickness=4)

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
    pr = (int(color_pallete_range * math.sin(math.radians(theta2)) + circle_center[0]),
          int(-color_pallete_range * math.cos(math.radians(theta2)) + circle_center[1]))  # yは上下反転
    cv2.circle(canvas, pr, color_pallete_circle_range, color, thickness=-1)

    return Image.fromarray(canvas)


images = []

for i_frame in range(0, 36):
    theta = 10*i_frame
    image = make_gif(theta)
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
