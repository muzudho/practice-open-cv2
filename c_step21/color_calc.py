"""(WIP) RGB値を計算します
"""


def convert_3heights_to_3bytes(n3bars_height, box_height):
    """３本のバーの縦幅ピクセルを、色に変えます"""
    n3rates = (
        n3bars_height[0]/box_height,
        n3bars_height[1]/box_height,
        n3bars_height[2]/box_height)
    return convert_3rates_to_3bytes(n3rates)


def convert_height_to_byte(bar_height, box_height):
    """バーの縦幅ピクセルを、色に変えます"""
    rate = bar_height/box_height
    return convert_rate_to_byte(rate)


def convert_byte_to_height(color, box_height):
    """色を、バーの縦幅ピクセルに変えます"""
    return int(color/255*box_height)


def convert_3rates_to_3bytes(n3rates):
    """３本のバーの縦幅ピクセルを、色に変えます"""
    return (
        convert_rate_to_byte(n3rates[0]),
        convert_rate_to_byte(n3rates[1]),
        convert_rate_to_byte(n3rates[2]))


def convert_rate_to_byte(rate):
    """バーの縦幅ピクセルを、色に変えます"""
    return int(rate*255)


def append_rank3_to_color_rate(step1_color_rate, bar_rate):
    """追加分のないバーが全体に対してどれぐらいの割合かを返します"""
    return (
        bar_rate[1] * step1_color_rate[0] + bar_rate[2],
        bar_rate[1] * step1_color_rate[1] + bar_rate[2],
        bar_rate[1] * step1_color_rate[2] + bar_rate[2])
