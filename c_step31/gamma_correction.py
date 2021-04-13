"""ガンマ補正を解除するためのフィルターです
"""

import math
from conf import ACCURACY

GAMMA = 2.2  # ガンマ補正指数


class GammaCorrection():
    """ガンマ補正を解除するためのフィルターです
    """

    def __init__(self):
        pass


def en_gamma_x(x_val):
    """線形空間から、ガンマ空間に変換します"""
    return x_val**GAMMA


def en_gamma(color):
    """線形空間から、ガンマ空間に変換します"""
    return (color[0]**GAMMA,
            color[1]**GAMMA,
            color[2]**GAMMA)


def de_gamma_x(x_val):
    """ガンマ補正を解除します"""
    if math.isclose(x_val, 0, rel_tol=ACCURACY, abs_tol=ACCURACY):
        return 1.0

    return x_val**-GAMMA


def de_gamma(color):
    """ガンマ補正を解除します"""
    return (de_gamma_x(color[0]),
            de_gamma_x(color[1]),
            de_gamma_x(color[2]))


def de_gamma_from_linear_x(x_val):
    """ガンマ補正がかかっていない空間に対して、ガンマ補正を解除します"""
    if math.isclose(x_val, 0, rel_tol=ACCURACY, abs_tol=ACCURACY):
        return 0.0

    # 逆さに考えます
    rev = (1.0-x_val)**GAMMA

    # 逆さに考えたのを、逆さにします。
    # これで 小さい数ほど底上げが大きくなります
    return 1.0 - rev


def de_gamma_from_linear(color):
    """ガンマ補正がかかっていない空間に対して、ガンマ補正を解除します"""
    return (de_gamma_from_linear_x(color[0]),
            de_gamma_from_linear_x(color[1]),
            de_gamma_from_linear_x(color[2]))
