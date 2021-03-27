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
    return new_color


def convert_3heights_to_3bytes(n3bars_height, box_height):
    """３本のバーの縦幅ピクセルを、色に変えます"""
    return (
        int(n3bars_height[0]/box_height*255),
        int(n3bars_height[1]/box_height*255),
        int(n3bars_height[2]/box_height*255),
    )


def calc_color_element_rates(color):
    """色成分比を求めます"""
    upper_bound = max(color[0], color[1], color[2])
    lower_bound = min(color[0], color[1], color[2])
    variable_height = upper_bound - lower_bound
    rank2_color = (
        color[0] - lower_bound,
        color[1] - lower_bound,
        color[2] - lower_bound)
    # RBGの比は求まった
    color_rates = (
        rank2_color[0] / variable_height,
        rank2_color[1] / variable_height,
        rank2_color[2] / variable_height)
    return color_rates


def to_be_red(color):
    """赤色にする"""
    new_color = sorted(color)
    return (new_color[0], new_color[2], new_color[1])


def to_be_green(color):
    """緑色にする"""
    new_color = sorted(color)
    return (new_color[1], new_color[0], new_color[2])


def to_be_blue(color):
    """青くする"""
    new_color = sorted(color)
    return (new_color[2], new_color[1], new_color[0])


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
