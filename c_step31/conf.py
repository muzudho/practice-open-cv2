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

# グリッド間隔
GRID_UNIT = 14
# GRID_UNIT = 16

# 色相環一周分のコマ数
# PHASE_COUNTS = 6
PHASE_COUNTS = 24  # 最低限、すべてのパターン数を押さえればいいとき（＾～＾）
# PHASE_COUNTS = 60  # 容量ケチりつつ、見栄えもそこそこ保ちたいとき（＾～＾）
# PHASE_COUNTS = 72  # 3*24
# PHASE_COUNTS = 168  # 7*24
# PHASE_COUNTS = 360  # 弧度法の精度で最大はこれ（＾～＾）
# PHASE_COUNTS = 8*360  # ラジアン値で誤差を測りたいとき（＾～＾）でも時間がかかってしまう（＾～＾）
# PHASE_COUNTS = 64*360  # 誤差チェック（＾～＾）

# フォント倍率
FONT_SCALE = 0.5

# 0～255なら、256
BAR_TICKS = 256
# BAR_TICKS = 60 # Vividのとき60にすると分かりやすいぜ（＾～＾）

if DE_GAMMA_FROM_LINEAR:
    # RGBの仕様から、ガンマ補正を解除する前提なら、こっち（＾～＾）
    L_M_U_NAME_LIST = [
        # 鮮やかさ2番
        (0.250, 0.750, 0.000, 'Bright'),  # Bright
        (0.125, 0.750, 0.125, 'Strong'),  # Strong
        (0.000, 0.750, 0.250, 'Deep'),  # Deep
        # 鮮やかさ3番
        (0.500, 0.500, 0.000, 'Light'),  # Light
        (0.372, 0.500, 0.166, 'Soft'),  # Soft
        (0.166, 0.500, 0.372, 'Dull'),  # Dull
        (0.000, 0.500, 0.500, 'Dark'),  # Dark
        # 鮮やかさ4番
        (0.750, 0.250, 0.000, 'Pale'),  # Pale
        (0.500, 0.250, 0.250, 'Light grayish'),  # Light grayish
        (0.250, 0.250, 0.500, 'Grayish'),  # Grayish
        (0.000, 0.250, 0.750, 'Dark grayish'),  # Dark grayish
        # 鮮やかさ1番
        (0.000, 1.000, 0.000, 'Vivid'),  # Vivid
    ]
else:
    # 合計 1.0 になるように 左から埋めろだぜ（＾～＾） 左の箱、真ん中の箱、右の箱の横幅の比だぜ（＾～＾）
    # ４つ目は見出し（＾～＾）
    L_M_U_NAME_LIST = [
        # 鮮やかさの説明
        #(0.0, 1.0, 0.0, 'Saturation 100%'),
        #(0.25, 0.5, 0.25, 'Saturation 50%'),
        #(0.375, 0.25, 0.375, 'Saturation 25%'),
        #(0.4375, 0.125, 0.4375, 'Saturation 12.5%'),

        # 明るさの説明
        #(0.75, 0.25, 0.0, 'Brightness ----> right'),
        #(0.5, 0.25, 0.25, 'Brightness ---> right'),
        #(0.25, 0.25, 0.5, 'Brightness --> right'),
        #(0.0, 0.25, 0.75, 'Brightness -> right'),

        # (0.63, 0.14,0.23,  'Tekitou 1'),  # 適当
        # (0.45, 0.51,0.04,  'Tekitou 2'),  # 適当
        # (0.34, 0.27,0.39,  'Tekitou 3'),  # 適当
        # (0.11, 0.89,0.0,  'Tekitou 4'),  # 適当
        # (0.02, 0.11,0.87,  'Tekitou 5'),  # 適当
        #
        # 色調
        # 鮮やかさ2番
        # (0.2, 0.7, 0.1, 'Bright'),  # Bright
        # (0.1, 0.7, 0.2, 'Strong'),  # Strong
        # (0.0, 0.7, 0.3, 'Deep'),  # Deep
        # 鮮やかさ3番
        # (0.6, 0.4, 0.0, 'Light'),  # Light
        # (0.5, 0.4, 0.1, 'Soft'),  # Soft
        # (0.3, 0.4, 0.3, 'Dull'),  # Dull
        # (0.2, 0.4, 0.4, 'Dark'),  # Dark
        # 鮮やかさ4番
        # (0.7, 0.3, 0.0, 'Pale'),  # Pale
        # (0.5, 0.3, 0.2, 'Light grayish'),  # Light grayish
        # (0.3, 0.3, 0.4, 'Grayish'),  # Grayish
        # (0.1, 0.3, 0.6, 'Dark grayish'),  # Dark grayish
        # 鮮やかさ1番
        # (0.0, 1.0, 0.0, 'Vivid'),  # Vivid
        # テストケース（鮮やかさ小）
        # (0.001, 0.999,0.0,  'Test case 1'),
        # テストケース（鮮やかさ小）
        # (0.999, 0.001,0.0,  'Test case 2'),
    ]
