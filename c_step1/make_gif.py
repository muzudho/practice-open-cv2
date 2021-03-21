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
width = 800
height = 400
channels = 3
background = 255

# 円、描画する画像を指定、座標（x,y),半径、色、線の太さ（-1は塗りつぶし）
canvas = np.full((height, width, channels), background, dtype=np.uint8)
cv2.circle(canvas, (200, 200), 180, black, thickness=2)

# 点R
center = (200, 200)  # x, y
range = 180
theta = 0
pr = (int(range * math.sin(math.radians(theta)) + center[0]),
      int(-range * math.cos(math.radians(theta)) + center[1]))  # yは上下反転
cv2.circle(canvas, pr, 10, red, thickness=-1)

# 点G
theta = 240  # 時計回り
pg = (int(range * math.sin(math.radians(theta)) + center[0]),
      int(-range * math.cos(math.radians(theta)) + center[1]))  # yは上下反転
cv2.circle(canvas, pg, 10, green, thickness=-1)

# 点B
theta = 120
pb = (int(range * math.sin(math.radians(theta)) + center[0]),
      int(-range * math.cos(math.radians(theta)) + center[1]))  # yは上下反転
cv2.circle(canvas, pb, 10, blue, thickness=-1)

# バーの筋
barr_x = 400
barg_x = 500
barb_x = 600

# 水平線R
# 線、描画する画像を指定、座標1点目、2点目、色、線の太さ
cv2.line(canvas, (pr[0], pr[1]), (barr_x, pr[1]), red, thickness=2)

# 水平線G
cv2.line(canvas, (pg[0], pg[1]), (barg_x, pg[1]), green, thickness=2)

# 水平線B
cv2.line(canvas, (pb[0], pb[1]), (barb_x, pb[1]), blue, thickness=2)

# バーR
bar_bottom = 380
bar_width = 98
bar_height = 380
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
