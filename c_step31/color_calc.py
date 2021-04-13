"""(WIP) RGB値を計算します
"""

from conf import BAR_TICKS


def convert_3bars_to_color(n3bars_pixel, total_pixels):
    """３本のバーの縦幅ピクセルを、色に変えます"""
    r_x = n3bars_pixel[0]/total_pixels
    g_x = n3bars_pixel[1]/total_pixels
    b_x = n3bars_pixel[2]/total_pixels

    return (r_x, g_x, b_x)
    #rrx = int((BAR_TICKS-1)*r_x)
    #ggx = int((BAR_TICKS-1)*g_x)
    #bbx = int((BAR_TICKS-1)*b_x)
    #
    # return (rrx, ggx, bbx)


def convert_pixel_to_color_element(element_pixels, total_pixels):
    """バーの縦幅ピクセルを、色に変えます"""
    rate = element_pixels/total_pixels
    return rate
    # return int(rate*(BAR_TICKS-1))
