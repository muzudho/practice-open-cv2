import cv2
import numpy as np
from PIL import Image
from datetime import datetime
import math

# 色 BGR
white = (255, 255, 255)
black = (16, 16, 16)
red = (250, 100, 100)
green = (100, 250, 100)
blue = (100, 100, 250)

images = []

# 描画する画像を作る,128を変えると色を変えれます 0黒→255白
canvas_width = 800
canvas_height = 400
channels = 3
background = 255

# キャンバス
canvas = np.full((canvas_height, canvas_width, channels),
                 background, dtype=np.uint8)

bar_top = 40
bar_max_height = 340
bar_bottom = bar_top + bar_max_height

circle_center = (200, 200)  # x, y
circle_range = 140
color_pallete_range = 175

# 円、描画する画像を指定、座標（x,y),半径、色、線の太さ（-1は塗りつぶし）
cv2.circle(canvas, circle_center, circle_range, black, thickness=2)

# 点R
theta = 0
pr = (int(circle_range * math.sin(math.radians(theta)) + circle_center[0]),
      int(-circle_range * math.cos(math.radians(theta)) + circle_center[1]))  # yは上下反転
cv2.circle(canvas, pr, 10, red, thickness=-1)

# 点G
theta = 240  # 時計回り
pg = (int(circle_range * math.sin(math.radians(theta)) + circle_center[0]),
      int(-circle_range * math.cos(math.radians(theta)) + circle_center[1]))  # yは上下反転
cv2.circle(canvas, pg, 10, green, thickness=-1)

# 点B
theta = 120
pb = (int(circle_range * math.sin(math.radians(theta)) + circle_center[0]),
      int(-circle_range * math.cos(math.radians(theta)) + circle_center[1]))  # yは上下反転
cv2.circle(canvas, pb, 10, blue, thickness=-1)

# バーの筋
barr_x = 450
barg_x = 550
barb_x = 650

# 水平線R
# 線、描画する画像を指定、座標1点目、2点目、色、線の太さ
cv2.line(canvas, (pr[0], pr[1]), (barr_x, pr[1]), red, thickness=2)

# 水平線G
cv2.line(canvas, (pg[0], pg[1]), (barg_x, pg[1]), green, thickness=2)

# 水平線B
cv2.line(canvas, (pb[0], pb[1]), (barb_x, pb[1]), blue, thickness=2)

# バーR
bar_width = 98
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

# 色円
valurr = 255-int(pr[1]/bar_max_height*255)
valurg = 255-int(pg[1]/bar_max_height*255)
valurb = 255-int(pb[1]/bar_max_height*255)
color = (valurr, valurg, valurb)
print(f"color={color}")
theta = 0
pr = (int(color_pallete_range * math.sin(math.radians(theta)) + circle_center[0]),
      int(-color_pallete_range * math.cos(math.radians(theta)) + circle_center[1]))  # yは上下反転
cv2.circle(canvas, pr, 20, color, thickness=-1)

images.append(Image.fromarray(canvas))

# cv2.imshow('canvas',canvas)
# cv2.imwrite('form.jpg',canvas)
date = datetime.now().strftime("%Y%m%d-%H%M%S")
path = f"out-{date}.gif"
fps = 1
duration_time = int(1000.0 / fps)
images[0].save(path,
               save_all=True,
               append_images=images[1:],
               optimize=False,
               duration=duration_time,
               loop=0)
