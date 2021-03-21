import cv2
import numpy as np
import copy
from PIL import Image
from datetime import datetime

BG_PATH = "./bg.png"   # 背景画像
FG_GIF_PATH = "./anime.gif"  # 合成アルファgif画像


def main():
    """ メイン関数
    """
    print("---start---")
    cap = cv2.VideoCapture(FG_GIF_PATH)  # gifファイルを読み込み
    bg_img = cv2.imread(BG_PATH)          # bg読み込み
    fps = cap.get(cv2.CAP_PROP_FPS)        # fps取得

    frames = []  # Pillowのimageリスト
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # bgに画像を合成
        alpha_scale = calc_resize_value(frame, bg_img)
        add_img = load_alphaImage(frame, alpha_scale)
        merged_img = merge_images(bg_img, add_img, 0, 0)

        # BGRをRGBにする
        img_array = cv2.cvtColor(merged_img, cv2.COLOR_BGR2RGB)

        # numpyのarrayからPillowのimage objectを作る
        im = Image.fromarray(img_array)
        frames.append(im)

    make_gif(frames, fps)
    print("---end---")


def calc_resize_value(f_img, bg_img):
    """合成するサイズを計算する関数
    """
    _, f_width = f_img.shape[:2]
    _, bg_width = bg_img.shape[:2]
    resize_value = bg_width / f_width
    return resize_value


def load_alphaImage(add_img, scale):
    """アルファ画像を読み込む関数
    """
    add_img = img_resize(add_img, scale)  # リサイズ
    return add_img


def img_resize(img, scale):
    """画像をリサイズする関数
    """
    h, w = img.shape[:2]
    img = cv2.resize(img, (int(w*scale), int(h*scale)))
    return img


def merge_images(bg, fg_alpha, fgx, fgy):
    """画像を合成する関数(s_xは画像を貼り付けるx座標、s_yは画像を貼り付けるy座標)
    """
    b, g, r = rgb_to_bgr_0_0(fg_alpha)  # 左上(0,0)を背景色として、BGRを取得

    # 背景色をマスク化
    bgr = np.array([b, g, r])
    work_img1 = bgrExtraction(fg_alpha, bgr, bgr)
    work_img1 = cv2.cvtColor(work_img1, cv2.COLOR_BGR2GRAY)
    work_img1 = cv2.bitwise_not(work_img1)

    work_img1 = cv2.cvtColor(work_img1, cv2.COLOR_GRAY2BGR)  # grayをBGRに
    work_img1 = work_img1 / 255.0    # 0.0〜1.0の値に変換

    fg = fg_alpha[:, :, :3]

    fgh, fgw, _ = fg.shape  # 前景画像の高さと幅を取得
    bgh, bgw, _ = bg.shape  # 背景画像の高さを幅を取得

    # 画像の大きさと開始座標を表示
    print("fgw:{} fgh:{} bgw:{} bgh:{} s({}, {})".format(
        fgw, fgh, bgw, bgh, fgx, fgy))

    work_img2 = copy.deepcopy(bg)  # 結果

    # 前景以外の部分を黒で合成
    work_img2[fgy:fgh+fgy, fgx:fgw+fgx] = (work_img2[fgy:fgh+fgy, fgx:fgw+fgx] * (
        1.0 - work_img1)).astype('uint8')
    # 合成
    work_img2[fgy:fgh+fgy, fgx:fgw+fgx] = (
        work_img2[fgy:fgh+fgy, fgx:fgw+fgx] + (fg * work_img1)).astype('uint8')

    return work_img2


def rgb_to_bgr_0_0(img):
    """左上の1pxのBGRの色を取得する関数
    """
    color = img[0, 0]  # 座標(y, x) = (0, 0)の色を取得
    b = color[0]
    g = color[1]
    r = color[2]
    return b, g, r


def bgrExtraction(image, bgrLower, bgrUpper):
    """BGRで特定の色のみを抽出する関数
    """
    img_mask = cv2.inRange(image, bgrLower, bgrUpper)  # BGRからマスクを作成

    # 元画像に、マスク画像をアンド結合
    img2 = cv2.bitwise_and(image, image, mask=img_mask)
    return img2


def make_gif(frames, fps):
    """gifを作成する関数
    """
    date = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"out-{date}.gif"
    duration_time = int(1000.0 / fps)
    print("duration:{}".format(duration_time))
    frames[0].save(path,
                   save_all=True,
                   append_images=frames[1:],
                   duration=duration_time,
                   loop=0)


if __name__ == '__main__':
    main()
