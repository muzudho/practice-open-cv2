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
PHASE_COUNTS = 360  # よく確認するにはこれだが、画像が多すぎる（＾～＾）
# PHASE_COUNTS = 8*360  # 誤差を測りたいとき（＾～＾）

# フォント倍率
FONT_SCALE = 0.5

# 0～255なら、256
BAR_TICKS = 256
# BAR_TICKS = 60 # Vividのとき60にすると分かりやすいぜ（＾～＾）
