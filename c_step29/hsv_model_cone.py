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

    # 彩度（円錐モデル）
    saturation = max_val - min_val
    if math.isclose(saturation, 0, rel_tol=ACCURACY, abs_tol=ACCURACY):
        return float('Nan')

    if red <= blue and green <= blue:
        hue_angle = 60 * (green-red)/saturation + 60
    elif green <= red and blue <= red:
        hue_angle = 60 * (blue-green)/saturation + 60
    elif red <= green and blue <= green:
        hue_angle = 60 * (blue-green)/saturation + 60

    return hue_angle
