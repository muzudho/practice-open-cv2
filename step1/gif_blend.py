import cv2
import numpy as np
import copy
from PIL import Image
from datetime import datetime

BG_PATH = "./bg.png"   # 背景画像
ALPHA_GIF_PATH = "./anime.gif"  # 合成アルファgif画像
ALPHA_SCALE = 1.0

# メイン関数


def main():
    print("---start---")
    cap = cv2.VideoCapture(ALPHA_GIF_PATH)  # gifファイルを読み込み
    bg_img = cv2.imread(BG_PATH)          # bg読み込み
    fps = cap.get(cv2.CAP_PROP_FPS)        # fps取得

    im_list = []  # Pillowのimageリスト
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # bgに画像を合成
        alpha_scale = calc_resize_value(frame, bg_img)
        add_img = load_alphaImage(frame, alpha_scale)
        result_img = merge_images(bg_img, add_img, 0, 0)

        # BGRをRGBにする
        img_array = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)

        # numpyのarrayからPillowのimage objectを作る
        im = Image.fromarray(img_array)
        im_list.append(im)

    make_gif(im_list, fps)
    print("---end---")

# 合成するサイズを計算する関数


def calc_resize_value(f_img, bg_img):
    _, f_width = f_img.shape[:2]
    _, bg_width = bg_img.shape[:2]
    resize_value = bg_width / f_width
    return resize_value

# アルファ画像を読み込む関数


def load_alphaImage(add_img, scale):
    add_img = img_resize(add_img, scale)  # リサイズ
    return add_img

# 画像をリサイズする関数


def img_resize(img, scale):
    h, w = img.shape[:2]
    img = cv2.resize(img, (int(w*scale), int(h*scale)))
    return img

# 画像を合成する関数(s_xは画像を貼り付けるx座標、s_yは画像を貼り付けるy座標)


def merge_images(bg, fg_alpha, s_x, s_y):
    b, g, r = get_bg_bgr(fg_alpha)  # 背景色を取得

    # 背景色をマスク化
    bgr = np.array([b, g, r])
    alpha = bgrExtraction(fg_alpha, bgr, bgr)
    alpha = cv2.cvtColor(alpha, cv2.COLOR_BGR2GRAY)
    alpha = cv2.bitwise_not(alpha)

    alpha = cv2.cvtColor(alpha, cv2.COLOR_GRAY2BGR)  # grayをBGRに
    alpha = alpha / 255.0    # 0.0〜1.0の値に変換

    fg = fg_alpha[:, :, :3]

    f_h, f_w, _ = fg.shape  # アルファ画像の高さと幅を取得
    b_h, b_w, _ = bg.shape  # 背景画像の高さを幅を取得

    # 画像の大きさと開始座標を表示
    print("f_w:{} f_h:{} b_w:{} b_h:{} s({}, {})".format(
        f_w, f_h, b_w, b_h, s_x, s_y))

    result_img = copy.deepcopy(bg)  # 結果

    result_img[s_y:f_h+s_y, s_x:f_w+s_x] = (result_img[s_y:f_h+s_y, s_x:f_w+s_x] * (
        1.0 - alpha)).astype('uint8')  # アルファ以外の部分を黒で合成
    result_img[s_y:f_h+s_y, s_x:f_w+s_x] = (
        result_img[s_y:f_h+s_y, s_x:f_w+s_x] + (fg * alpha)).astype('uint8')  # 合成

    return result_img

# 左上の1pxのBGRの色を取得する関数


def get_bg_bgr(img):
    color = img[0, 0]  # 座標(y, x) = (0, 0)の色を取得
    b = color[0]
    g = color[1]
    r = color[2]
    return b, g, r

# BGRで特定の色のみを抽出する関数


def bgrExtraction(image, bgrLower, bgrUpper):
    img_mask = cv2.inRange(image, bgrLower, bgrUpper)  # BGRからマスクを作成
    result = cv2.bitwise_and(image, image, mask=img_mask)  # 元画像とマスクを合成
    return result

# gifを作成する関数


def make_gif(im_list, fps):
    date = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"out-{date}.gif"
    duration_time = int(1000.0 / fps)
    print("duration:{}".format(duration_time))
    im_list[0].save(path, save_all=True, append_images=im_list[1:],
                    duration=duration_time, loop=0)


if __name__ == '__main__':
    main()
