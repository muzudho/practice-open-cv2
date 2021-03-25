"""RGB値を計算します
"""

import math


def calc_step1(theta):
    """色変換計算ステップ１"""
    red_y = (math.cos(math.radians(theta))+1)/2
    green_y = (math.cos(math.radians(theta-120))+1)/2
    blue_y = (math.cos(math.radians(theta+120))+1)/2
    return (red_y, green_y, blue_y)


def calc_step2(color, upper_bound, height, ceil_height, base_line):
    """色変換計算ステップ２"""
    expected_height = height - ceil_height - base_line
    zoom = (upper_bound-base_line) / expected_height
    new_color = (
        int((color[0]-base_line)/zoom+base_line),
        int((color[1]-base_line)/zoom+base_line),
        int((color[2]-base_line)/zoom+base_line))
    print(
        f"color={color} upper_bound={upper_bound} height={height} base_line={base_line} zoom={zoom} new_color={new_color}")
    return new_color


def calc_color(theta, bar_rate):
    """(r,g,b)を返します
    """

    # 下駄
    offset = 255*bar_rate[2]

    color = calc_step1(theta)
    red_y = 255*bar_rate[1]*color[0]
    green_y = 255*bar_rate[1]*color[1]
    blue_y = 255*bar_rate[1]*color[2]

    red_y = int(red_y+offset)
    green_y = int(green_y+offset)
    blue_y = int(blue_y+offset)

    return (red_y, green_y, blue_y)
