"""(WIP) RGB値を計算します
"""

from conf import RGB_BAR_TICKS


def convert_3bars_to_3bytes(n3bars_pixel, total_pixels):
    """３本のバーの縦幅ピクセルを、色に変えます"""
    r_x = n3bars_pixel[0]/total_pixels
    g_x = n3bars_pixel[1]/total_pixels
    b_x = n3bars_pixel[2]/total_pixels

    rrx = int((RGB_BAR_TICKS-1)*r_x)
    ggx = int((RGB_BAR_TICKS-1)*g_x)
    bbx = int((RGB_BAR_TICKS-1)*b_x)

    return (rrx, ggx, bbx)


def convert_3pixels_to_3bytes(n3bars_pixel, total_pixels):
    """３本のバーの縦幅ピクセルを、色に変えます"""
    n3rates = (
        n3bars_pixel[0]/total_pixels,
        n3bars_pixel[1]/total_pixels,
        n3bars_pixel[2]/total_pixels)
    return convert_3rates_to_3bytes(n3rates)


def convert_pixel_to_byte(element_pixels, total_pixels):
    """バーの縦幅ピクセルを、色に変えます"""
    rate = element_pixels/total_pixels
    return convert_rate_to_byte(rate)


def convert_byte_to_pixel(color, pixels):
    """色を、バーの縦幅ピクセルに変えます"""
    return int(color/(RGB_BAR_TICKS-1)*pixels)


def convert_3rates_to_3bytes(n3rates):
    """３本のバーの縦幅ピクセルを、色に変えます"""
    return (
        convert_rate_to_byte(n3rates[0]),
        convert_rate_to_byte(n3rates[1]),
        convert_rate_to_byte(n3rates[2]))


def convert_rate_to_byte(rate):
    """バーの縦幅ピクセルを、色に変えます"""
    return int(rate*(RGB_BAR_TICKS-1))


def append_rank3_to_color_rate(step1_color_rate, bar_rate):
    """追加分のないバーが全体に対してどれぐらいの割合かを返します"""
    return (
        bar_rate[1] * step1_color_rate[0] + bar_rate[2],
        bar_rate[1] * step1_color_rate[1] + bar_rate[2],
        bar_rate[1] * step1_color_rate[2] + bar_rate[2])
