"""ガンマ補正を解除するためのフィルターです
"""

GAMMA = 2.2  # ガンマ補正指数


class GammaCorrection():
    """ガンマ補正を解除するためのフィルターです
    """

    def __init__(self):
        pass


def en_gamma(x_val):
    """線形空間から、ガンマ空間に変換します"""
    return x_val**GAMMA


def de_gamma(x_val):
    """ガンマ補正を解除します"""
    return 1.0 - x_val**GAMMA
