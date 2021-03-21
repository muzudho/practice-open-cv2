import cv2
import numpy as np
from PIL import Image
from datetime import datetime

# 色 BGR
black = (16, 16, 16)

images = []

# 描画する画像を作る,128を変えると色を変えれます 0黒→255白
width = 800
height = 400
canvas = np.full((height, width, 3), 255, dtype=np.uint8)

# 円、描画する画像を指定、座標（x,y),半径、色、線の太さ（-1は塗りつぶし）
cv2.circle(canvas, (200, 200), 180, black, thickness=2)
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
