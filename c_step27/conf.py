"""設定
* 横幅は 450px 程度以下
  * crieitブログに貼りつけるとき、横幅が広すぎると圧縮されて gifアニメ ではなくなってしまう
* ファイルサイズは 2MB 以下
  * crieitブログの画像貼付け制限
"""

# グリッド間隔
GRID_UNIT = 14
# GRID_UNIT = 16

# 色相環一周分のコマ数
# PHASE_COUNTS = 6
# PHASE_COUNTS = 24
# PHASE_COUNTS = 60
PHASE_COUNTS = 360  # 弧度法の精度ではこれ（＾～＾）
# PHASE_COUNTS = 8*360  # 誤差を測りたいとき（＾～＾）でも時間がかかってしまう（＾～＾）
# PHASE_COUNTS = 64*360  # 誤差チェック（＾～＾）

# フォント倍率
FONT_SCALE = 0.5

# 0～255なら、256
BAR_TICKS = 256
# BAR_TICKS = 60 # Vividのとき60にすると分かりやすいぜ（＾～＾）


# とりあえず 11トーン
U_M_L_NAME_LIST = [
    # 鮮やかさの説明
    (0.0, 1.0, 0.0, 'Saturation 100%'),  # 適当
    (0.25, 0.5, 0.25, 'Saturation 50%'),  # 適当
    (0.375, 0.25, 0.375, 'Saturation 25%'),  # 適当
    (0.4375, 0.125, 0.4375, 'Saturation 12.5%'),  # 適当

    # (0.23, 0.14, 0.63, 'Tekitou 1'),  # 適当
    # (0.04, 0.51, 0.45, 'Tekitou 2'),  # 適当
    # (0.39, 0.27, 0.34, 'Tekitou 3'),  # 適当
    # (0.0, 0.89, 0.11, 'Tekitou 4'),  # 適当
    # (0.87, 0.11, 0.02, 'Tekitou 5'),  # 適当
    #
    # 鮮やかさ2番
    # (0.1, 0.7, 0.2, 'Bright'),  # Bright
    # (0.2, 0.7, 0.1, 'Strong'),  # Strong
    # (0.3, 0.7, 0.0, 'Deep'),  # Deep
    # 鮮やかさ3番
    # (0.0, 0.4, 0.6, 'Light'),  # Light
    # (0.1, 0.4, 0.5, 'Soft'),  # Soft
    # (0.3, 0.4, 0.3, 'Dull'),  # Dull
    # (0.4, 0.4, 0.2, 'Dark'),  # Dark
    # 鮮やかさ4番
    # (0.0, 0.3, 0.7, 'Pale'),  # Pale
    # (0.2, 0.3, 0.5, 'Light grayish'),  # Light grayish
    # (0.4, 0.3, 0.3, 'Grayish'),  # Grayish
    # (0.6, 0.3, 0.1, 'Dark grayish'),  # Dark grayish
    # 鮮やかさ1番
    # (0.0, 1.0, 0.0, 'Vivid'),  # Vivid
    # テストケース（鮮やかさ小）
    # (0.0, 0.999, 0.001, 'Test case 1'),
    # テストケース（鮮やかさ小）
    # (0.0, 0.001, 0.999, 'Test case 2'),
]
