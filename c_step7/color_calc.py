"""RGB値を計算します
"""

import math


def calc_color(theta, bar_rate):
    """(r,g,b)を返します
    """

    # 下駄
    offset = 255*bar_rate[2]

    red_y = 255*bar_rate[1]*math.cos(math.radians(theta))
    green_y = 255*bar_rate[1]*math.cos(math.radians(theta-120))
    blue_y = 255*bar_rate[1]*math.cos(math.radians(theta+120))

    red_y = int(red_y+offset)
    green_y = int(green_y+offset)
    blue_y = int(blue_y+offset)

    return (red_y, green_y, blue_y)
