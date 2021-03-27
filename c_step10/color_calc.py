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
    if zoom == 0:
        new_color = (
            int(base_line),
            int(base_line),
            int(base_line))
    else:
        new_color = (
            int((color[0]-base_line)/zoom+base_line),
            int((color[1]-base_line)/zoom+base_line),
            int((color[2]-base_line)/zoom+base_line))
    # print(
    #    f"color={color} upper_bound={upper_bound} height={height} base_line={base_line} zoom={zoom} new_color={new_color}")
    return new_color


def append_rank3_to_color(color, bar_rate):
    """(red_height_px, green_height_px, blue_height_px)を返します
    """

    rank2_red_px = 255*bar_rate[1]*color[0]
    rank2_green_px = 255*bar_rate[1]*color[1]
    rank2_blue_px = 255*bar_rate[1]*color[2]

    # 下駄
    offset = 255*bar_rate[2]
    rank23_red_px = int(rank2_red_px+offset)
    rank23_green_px = int(rank2_green_px+offset)
    rank23_blue_px = int(rank2_blue_px+offset)

    return (rank23_red_px, rank23_green_px, rank23_blue_px)
