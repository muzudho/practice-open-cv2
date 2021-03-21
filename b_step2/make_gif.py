import cv2
import numpy as np
from PIL import Image
from datetime import datetime

images = []

# 描画する画像を作る,128を変えると色を変えれます 0黒→255白
canvas = np.full((250, 600, 3), 128, dtype=np.uint8)

new_img = Image.fromarray(canvas)
images.append(new_img)

# 長方形,描画する画像,座標1点目、座標2点目、色、線の太さ（-1は塗りつぶし）
# BGR
green = (0, 255, 0)
blue = (255, 0, 0)
cv2.rectangle(canvas, (10, 10), (110, 110), green, thickness=1)
cv2.rectangle(canvas, (10, 120), (110, 220), blue, thickness=-1)

new_img = Image.fromarray(canvas)
images.append(new_img)


# 線、描画する画像を指定、座標1点目、2点目、色、線の太さ
white = (255, 255, 255)
cv2.line(canvas, (120, 10), (220, 110), white, thickness=1)

new_img = Image.fromarray(canvas)
images.append(new_img)

# 円、描画する画像を指定、座標（x,y),半径、色、線の太さ（-1は塗りつぶし）
red = (0, 0, 255)
cv2.circle(canvas, (300, 60), 50, red, thickness=5)
cv2.circle(canvas, (300, 170), 50, red, thickness=-1)

new_img = Image.fromarray(canvas)
images.append(new_img)

# 楕円、描画する画像を指定、座標(x,y),xyの半径、角度,色、線の太さ(-1は塗りつぶし)
cv2.ellipse(canvas, ((400, 60), (10, 50), 0), white, thickness=1)
cv2.ellipse(canvas, ((400, 170), (50, 50), 0), white, thickness=-1)
cv2.ellipse(canvas, ((500, 60), (50, 10), 0), white, thickness=1)
cv2.ellipse(canvas, ((500, 170), (50, 10), 30), white, thickness=-1)

new_img = Image.fromarray(canvas)
images.append(new_img)

# cv2.imshow('canvas',canvas)
# cv2.imwrite('form.jpg',canvas)
date = datetime.now().strftime("%Y%m%d_%H%M%S")
path = f"out-{date}.gif"
images[0].save(path,
               save_all=True,
               append_images=images[1:],
               optimize=False,
               loop=0)
