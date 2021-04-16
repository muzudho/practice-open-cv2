"""設定
* 横幅は 450px 程度以下
  * crieitブログに貼りつけるとき、横幅が広すぎると圧縮されて gifアニメ ではなくなってしまう
* ファイルサイズは 2MB 以下
  * crieitブログの画像貼付け制限
"""

# ガンマ補正の掛かっていない空間に対して、ガンマ補正を解除します
DE_GAMMA_FROM_LINEAR = True

# 浮動小数点精度。ネイピアの対数表の精度をリスペクトして、適当に7桁にしたんで深い意味ない（＾～＾）
ACCURACY = 0.0000001

# キャンバス設定
CANVAS_CHANNELS = 3
# グリッド間隔
GRID_UNIT = 16
# OSによってフォント・ファイルの場所が違うので注意
TRUE_TYPE_FONT = 'C:/Windows/Fonts/meiryo.ttc'

# フォント倍率
FONT_SCALE = 0.5
