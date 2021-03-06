"""[OpenCVで日本語フォントを描写する　を関数化する　を汎用的にする](https://qiita.com/mo256man/items/b6e17b5a66d1ea13b5e3)
[python Pillow（PIL)で日本語描画](https://emotionexplorer.blog.fc2.com/blog-entry-114.html)
"""

import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont


def cv2_put_text_5(img, text, org, fontFace, fontScale, color, mode=0):
    # cv2.putText()にないオリジナル引数「mode」　orgで指定した座標の基準
    # 0（デフォ）＝cv2.putText()と同じく左下　1＝左上　2＝中央

    # テキスト描写域を取得
    font_pil = ImageFont.truetype(font=fontFace, size=fontScale)
    dummy_draw = ImageDraw.Draw(Image.new("RGB", (0, 0)))
    text_w, text_h = dummy_draw.textsize(text, font=font_pil)
    text_b = int(0.1 * text_h)  # バグにより下にはみ出る分の対策

    # テキスト描写域の左上座標を取得（元画像の左上を原点とする）
    left_x, left_y = org
    offset_x = [0, 0, text_w//2]
    offset_y = [text_h, 0, (text_h+text_b)//2]
    x_0 = left_x - offset_x[mode]
    y_0 = left_y - offset_y[mode]
    img_h, img_w = img.shape[:2]

    # 画面外なら何もしない
    if not ((-text_w < x_0 < img_w) and (-text_b-text_h < y_0 < img_h)):
        print("out of bounds")
        return img

    # テキスト描写域の中で元画像がある領域の左上と右下（元画像の左上を原点とする）
    x_1, y_1 = max(x_0, 0), max(y_0, 0)
    x_2, y_2 = min(x_0+text_w, img_w), min(y_0+text_h+text_b, img_h)

    # テキスト描写域と同サイズの黒画像を作り、それの全部もしくは一部に元画像を貼る
    text_area = np.full((text_h+text_b, text_w, 3), (0, 0, 0), dtype=np.uint8)
    text_area[y_1-y_0:y_2-y_0, x_1-x_0:x_2-x_0] = img[y_1:y_2, x_1:x_2]

    # それをPIL化し、フォントを指定してテキストを描写する（色変換なし）
    img_pil = Image.fromarray(text_area)
    draw = ImageDraw.Draw(img_pil)
    draw.text(xy=(0, 0), text=text, fill=color, font=font_pil)

    # PIL画像をOpenCV画像に戻す（色変換なし）
    text_area = np.array(img_pil, dtype=np.uint8)

    # 元画像の該当エリアを、文字が描写されたものに更新する
    img[y_1:y_2, x_1:x_2] = text_area[y_1-y_0:y_2-y_0, x_1-x_0:x_2-x_0]

    return img


def main():
    """日本語の表示"""
    img = np.full((200, 400, 3), (160, 160, 160), dtype=np.uint8)
    img_h, img_w = img.shape[:2]

    # OSによってフォント・ファイルの場所が違うので注意
    font_pil = "C:/Windows/Fonts/meiryo.ttc"
    size = 30
    text = "日本語も\n可能なり"
    color = (255, 0, 0)

    positions = [(-img_w, -img_h),                 # これは画像外にあり描写されない
                 (0, 0), (0, img_h//2), (0, img_h),
                 (img_w//2, 0), (img_w//2, img_h//2), (img_w//2, img_h),
                 (img_w, 0), (img_w, img_h//2), (img_w, img_h)]

    for pos in positions:
        img = cv2.circle(img, pos, 60, (0, 0, 255), 3)
        img = cv2_put_text_5(img=img,
                             text=text,
                             org=pos,          # 円の中心と同じ座標を指定した
                             fontFace=font_pil,
                             fontScale=size,
                             color=color,
                             mode=2)           # 今指定した座標は文字描写域の中心だぞ

    cv2.imshow("", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
