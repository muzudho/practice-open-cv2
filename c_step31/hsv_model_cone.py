"""HSVモデル（円錐モデル）
"""

import math
from conf import ACCURACY


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
    saturation = max_val - min_val
    if math.isclose(saturation, 0, rel_tol=ACCURACY, abs_tol=ACCURACY):
        return float('Nan')

    if max_val == red:
        hue_rate = (green-blue)/saturation % 6
    elif max_val == green:
        hue_rate = (blue-red)/saturation + 2
    elif max_val == blue:
        hue_rate = (red-green)/saturation + 4

    hue_angle = 60 * hue_rate

    return hue_angle


def to_color(hue_angle, saturation, max_val):
    """色を求めます。
    Parameters
    ==========
    angle : int
        色相(Hue)。0～359
    """
    chroma = max_val * saturation
    hue_rate = hue_angle / 60
    x_val = chroma * (1 - abs(hue_rate % 2 - 1))

    if 0 <= hue_rate < 1:
        red = chroma
        green = x_val
        blue = 0
    elif 1 <= hue_rate < 2:
        red = x_val
        green = chroma
        blue = 0
    elif 2 <= hue_rate < 3:
        red = 0
        green = chroma
        blue = x_val
    elif 3 <= hue_rate < 4:
        red = 0
        green = x_val
        blue = chroma
    elif 4 <= hue_rate < 5:
        red = x_val
        green = 0
        blue = chroma
    elif 5 <= hue_rate < 6:
        red = chroma
        green = 0
        blue = x_val

    min_val = max_val - chroma
    red += min_val
    green += min_val
    blue += min_val

    return (red, green, blue)
