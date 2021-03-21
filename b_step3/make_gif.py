import cv2
import numpy as np
from PIL import Image
from datetime import datetime

images = []

# 描画する画像を作る,128を変えると色を変えれます 0黒→255白
#width = 300
#height = 300
#canvas = np.full((height, width, 3), 128, dtype=np.uint8)
#new_img = Image.fromarray(canvas)
# images.append(new_img)

# `im_arr1` - 大きな配列
im_arr1 = cv2.imread("./img/20210321anime1.png")
print(f"im_arr1={im_arr1}")
cv2.imshow('Title', im_arr1)
cv2.waitKey(0)
cv2.destroyAllWindows()
images.append(Image.fromarray(im_arr1))

im_arr1 = cv2.imread("./img/20210321anime2.png")
images.append(Image.fromarray(im_arr1))

im_arr1 = cv2.imread("./img/20210321anime3.png")
images.append(Image.fromarray(im_arr1))

im_arr1 = cv2.imread("./img/20210321anime4.png")
images.append(Image.fromarray(im_arr1))

im_arr1 = cv2.imread("./img/20210321anime5.png")
images.append(Image.fromarray(im_arr1))

# cv2.imshow('canvas',canvas)
# cv2.imwrite('form.jpg',canvas)
date = datetime.now().strftime("%Y%m%d_%H%M%S")
path = f"out-{date}.gif"
images[0].save(path,
               save_all=True,
               append_images=images[1:],
               optimize=False,
               loop=0)
