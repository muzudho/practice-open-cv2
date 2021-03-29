"""(WIP) RGB値を計算します
"""

import math


def calc_step1(theta):
    """色変換計算ステップ１"""
    red_rate = (math.cos(math.radians(theta))+1)/2
    green_rate = (math.cos(math.radians(theta-120))+1)/2
    blue_rate = (math.cos(math.radians(theta+120))+1)/2
    return (red_rate, green_rate, blue_rate)


def calc_step2(n3bars_h, diameter):
    """フィットしたときの差分
    n3bars_h : (int,int,int)
        ２段目の箱の中の３本のバーの縦幅
    diameter : int
        ２段目の箱の縦幅
    """

    if diameter == 0:
        return (0, 0, 0)

    longest = max(n3bars_h[0], n3bars_h[1], n3bars_h[2])
    shortest = min(n3bars_h[0], n3bars_h[1], n3bars_h[2])
    inner = longest - shortest

    zoom = inner / diameter
    # print(f"zoom={zoom} inner={inner} diameter={diameter}")

    inner_r = n3bars_h[0] - shortest
    inner_g = n3bars_h[1] - shortest
    inner_b = n3bars_h[2] - shortest

    fit_r = int(inner_r / zoom)
    fit_g = int(inner_g / zoom)
    fit_b = int(inner_b / zoom)

    r_bar_delta = fit_r - n3bars_h[0]
    g_bar_delta = fit_g - n3bars_h[1]
    b_bar_delta = fit_b - n3bars_h[2]

    return (r_bar_delta, g_bar_delta, b_bar_delta)


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


def calc_color_element_rates(color):
    """(WIP) 色成分比を求めます"""
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
    # 弧度法に変換
    color_degrees = (
        color_rates[0] * 360,
        color_rates[1] * 360,
        color_rates[2] * 360)
    # その結果、 0, x, 360 に分別できる３値が返ってくる。ここで x は 0 <= x <= 360。
    # まず 360 が 2つあるものを除外します。
    if color_degrees[0] == 360 and color_degrees[1] == 360:
        # イエロー
        return color_rates, 60  # 12時が0°の時計回り
    if color_degrees[1] == 360 and color_degrees[2] == 360:
        # シアン
        return color_rates, 180
    if color_degrees[0] == 360 and color_degrees[2] == 360:
        # マゼンタ
        return color_rates, 300
    # 0 が２つあるものを除外します。
    if color_degrees[1] == 0 and color_degrees[2] == 0:
        # 赤
        return color_rates, 0
    if color_degrees[0] == 0 and color_degrees[2] == 0:
        # 緑
        return color_rates, 120
    if color_degrees[0] == 0 and color_degrees[1] == 0:
        # 青
        return color_rates, 240
    # これで、 0, x, 360 に分別できる３値が返ってくる。ここで x は 0 < x < 360。
    x_rate = sorted(color_rates)[1]
    # print(f"x_rate={x_rate}")
    # 0 と 360 がどこにあるかで、オレンジ相、黄緑相、エメラルドグリーン相、
    # ドジャースブルー相、インディゴ相、クリムゾン相 の６つに分けれる。
    # また、 x は、 オレンジ相では昇順、黄緑相では降順になるなど、交互になる。
    if color_degrees[0] == 360 and color_degrees[2] == 0:
        # オレンジ相 (0°～60°) では、 x は上昇緑
        return color_rates, math.asin(x_rate)
    if color_degrees[1] == 360 and color_degrees[2] == 0:
        # 黄緑相 (60°～120°) では、 x は下降赤
        return color_rates, math.asin(x_rate)
    if color_degrees[0] == 0 and color_degrees[1] == 360:
        # エメラルドグリーン相 (120°～180°) では、 x は上昇青
        return color_rates, math.asin(x_rate)
    if color_degrees[0] == 0 and color_degrees[2] == 360:
        # ドジャースブルー相 (180°～240°) では、 x は下降緑
        return color_rates, math.asin(x_rate)
    if color_degrees[1] == 0 and color_degrees[2] == 360:
        # インディゴ相 (240°～300°) では、 x は上昇赤
        return color_rates, math.asin(x_rate)
    if color_degrees[0] == 360 and color_degrees[1] == 0:
        # クリムゾン相 (300°～360°) では、 x は下降青
        return color_rates, math.asin(x_rate)
    expected_theta = sorted(color_rates)[1]

#    # 元が cos(theta) だったので、acos(theta) したらどうか？
#    colors_theta = (
#        math.acos(color_rates[0]),
#        math.acos(color_rates[1]),
#        math.acos(color_rates[2]))
#    # 緑は -120°、 青は 120° 足しているから、逆に引いたらどうか
#    colors_theta = (
#        colors_theta[0],
#        colors_theta[1] + math.radians(120),
#        colors_theta[2] - math.radians(120),
#    )

    return color_rates, expected_theta


def to_be_red(color):
    """(WIP) 赤色にする"""
    new_color = sorted(color)
    return (new_color[0], new_color[2], new_color[1])


def to_be_green(color):
    """(WIP) 緑色にする"""
    new_color = sorted(color)
    return (new_color[1], new_color[0], new_color[2])


def to_be_blue(color):
    """(WIP) 青くする"""
    new_color = sorted(color)
    return (new_color[2], new_color[1], new_color[0])


def append_rank3_to_color_rate(step1_color_rate, bar_rate):
    """追加分のないバーが全体に対してどれぐらいの割合かを返します"""
    return (
        bar_rate[1] * step1_color_rate[0] + bar_rate[2],
        bar_rate[1] * step1_color_rate[1] + bar_rate[2],
        bar_rate[1] * step1_color_rate[2] + bar_rate[2])
