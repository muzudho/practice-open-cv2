import cv2
import numpy as np
from PIL import Image
from datetime import datetime
import math

# 色 BGR
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
cx = 200
cy = 200
range = 180
theta = 0
x = int(range * math.sin(math.radians(theta)) + cx)
y = int(-range * math.cos(math.radians(theta)) + cy)  # yは上下反転
cv2.circle(canvas, (x, y), 10, red, thickness=-1)

# 点G
theta = 240  # 時計回り
x = int(range * math.sin(math.radians(theta)) + cx)
y = int(-range * math.cos(math.radians(theta)) + cy)  # yは上下反転
cv2.circle(canvas, (x, y), 10, green, thickness=-1)

# 点B
theta = 120
x = int(range * math.sin(math.radians(theta)) + cx)
y = int(-range * math.cos(math.radians(theta)) + cy)  # yは上下反転
cv2.circle(canvas, (x, y), 10, blue, thickness=-1)

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
