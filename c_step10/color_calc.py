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
    # 弧度法に変換
    color_rates = (
        color_rates[0] * 360,
        color_rates[1] * 360,
        color_rates[2] * 360)
    # その結果、 0, x, 360 に分別できる３値が返ってくる。ここで x は 0 <= x <= 360。
    # まず 360 が 2つあるものを除外します。
    if color_rates[0] == 360 and color_rates[1] == 360:
        # イエロー
        return color_rates, 60  # 12時が0°の時計回り
    if color_rates[1] == 360 and color_rates[2] == 360:
        # シアン
        return color_rates, 180
    if color_rates[0] == 360 and color_rates[2] == 360:
        # マゼンタ
        return color_rates, 300
    # 0 が２つあるものを除外します。
    if color_rates[1] == 0 and color_rates[2] == 0:
        # 赤
        return color_rates, 0
    if color_rates[0] == 0 and color_rates[2] == 0:
        # 緑
        return color_rates, 120
    if color_rates[0] == 0 and color_rates[1] == 0:
        # 青
        return color_rates, 240
    # これで、 0, x, 360 に分別できる３値が返ってくる。ここで x は 0 < x < 360。
    # 0 と 360 がどこにあるかで、オレンジ相、黄緑相、エメラルドグリーン相、
    # ドジャースブルー相、インディゴ相、クリムゾン相 の６つに分けれる。
    if color_rates[0] == 360 and color_rates[2] == 0:
        # オレンジ相 (0°～60°)
        return color_rates, 400
    if color_rates[1] == 360 and color_rates[2] == 0:
        # 黄緑相 (60°～120°)
        return color_rates, 500
    if color_rates[0] == 0 and color_rates[1] == 360:
        # エメラルドグリーン相 (120°～180°)
        return color_rates, 600
    if color_rates[0] == 0 and color_rates[2] == 360:
        # ドジャースブルー相 (180°～240°)
        return color_rates, 700
    if color_rates[1] == 0 and color_rates[2] == 360:
        # インディゴ相 (240°～300°)
        return color_rates, 800
    if color_rates[0] == 360 and color_rates[1] == 0:
        # クリムゾン相 (300°～360°)
        return color_rates, 900
    three_nums = sorted(color_rates)
    expected_theta = three_nums[1]

    """
    # 元が cos(theta) だったので、acos(theta) したらどうか？
    colors_theta = (
        math.acos(color_rates[0]),
        math.acos(color_rates[1]),
        math.acos(color_rates[2]))
    # 緑は -120°、 青は 120° 足しているから、逆に引いたらどうか
    colors_theta = (
        colors_theta[0],
        colors_theta[1] + math.radians(120),
        colors_theta[2] - math.radians(120),
    )
    """

    return color_rates, expected_theta


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
