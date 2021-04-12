"""HSVモデル（円錐モデル）
"""

import math

ACCURACY = 0.0000001  # 浮動小数点精度。ネイピアの対数表の精度をリスペクトして、適当に7桁にしたんで深い意味ない（＾～＾）


def to_hue_angle(color):
    """色の色相（Hue）を求めます。
    Parameters
    ==========
    color : (float, float, float)
        左から R, G, B。 0.0～1.0
    """
    red = color[0]
    green = color[1]
    blue = color[2]
    max_val = max(red, green, blue)
    min_val = min(red, green, blue)

    # モノクロさ、逆に言うと彩度（円錐モデル）
    chroma = max_val - min_val
    if math.isclose(chroma, 0, rel_tol=ACCURACY, abs_tol=ACCURACY):
        return float('Nan')

    if max_val == red:
        hue_rate = (green-blue)/chroma % 6
    elif max_val == green:
        hue_rate = (blue-red)/chroma + 2
    elif max_val == blue:
        hue_rate = (red-green)/chroma + 4

    hue_angle = 60 * hue_rate

    return hue_angle
