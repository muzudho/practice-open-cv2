"""HULモデル
MIT LICENSE

HSVモデルの仲間で、
色相と色調を扱うライブラリの実装です。
"""

import math


def inverse_func(color):
    """逆関数"""
    red = color[0]
    green = color[1]
    blue = color[2]
    if red == green == blue:
        raise Exception(f"monocro color=({red}, {green}, {blue})")

    upper = max(red, green, blue)
    lower = min(red, green, blue)
    # 1本はU、1本はL なので、U と L を消せば動いているバーの長さになります
    bar_length = red + green + blue - upper - lower
    width = bar_length - lower
    # print(f"red={red} green={green} blue={blue} bar_length={bar_length}")

    # 弧度法
    theta = 0

    if green == blue and red == upper:
        return 0, upper, lower, "A1"
    if red == green and blue == lower:
        return 60, upper, lower, "A2"
    if red == blue and green == upper:
        return 120, upper, lower, "A3"
    if green == blue and red == lower:
        return 180, upper, lower, "A4"
    if red == green and blue == upper:
        return 240, upper, lower, "A5"
    if red == blue and green == lower:
        return 300, upper, lower, "A6"

    diameter = upper - lower
    radius = diameter / 2
    if red == upper and blue == lower:
        # パターン１ (0°～30°)
        if width < diameter/2:
            theta = math.degrees(math.asin(width/diameter))
            return theta, upper, lower, "B1"
        # パターン２ (30°～60°)
        theta = 30 - math.degrees(math.asin((diameter - width)/diameter)) + 30
        return theta, upper, lower, "B2"
    if green == upper and blue == lower:
        # パターン３
        if diameter/2 < width:
            theta = math.degrees(math.asin((diameter - width)/diameter)) + 60
            return theta, upper, lower, "B3"
        # パターン４ (赤バーが下半分で減っていっている)
        theta = 30 - math.degrees(math.asin(width/diameter)) + 90
        return theta, upper, lower, "B4"
    if red == lower and green == upper:
        # パターン５
        if width < diameter/2:
            theta = math.degrees(math.asin(width/diameter)) + 120
            return theta, upper, lower, "B5"
        # パターン６
        theta = 30 - \
            math.degrees(math.asin((diameter - width)/diameter)) + 150
        return theta, upper, lower, "B6"
    if red == lower and blue == upper:
        if diameter/2 < width:
            # パターン７
            theta = math.degrees(math.asin((diameter - width)/diameter)) + 180
            return theta, upper, lower, "B7"
        # パターン８
        theta = 30 - math.degrees(math.asin(width/diameter)) + 210
        return theta, upper, lower, "B8"
    if green == lower and blue == upper:
        # パターン９
        if width < diameter/2:
            theta = math.degrees(math.asin(width/diameter)) + 240
            return theta, upper, lower, "B9"
        # パターン１０
        theta = 30 - \
            math.degrees(math.asin((diameter - width)/diameter)) + 270
        return theta, upper, lower, "B10"
    if red == upper and green == lower:
        # パターン１１
        if diameter/2 < width:
            theta = math.degrees(math.asin((diameter - width)/diameter)) + 300
            return theta, upper, lower, "B11"
        # パターン１２
        theta = 30 - math.degrees(math.asin(width/diameter)) + 330
        return theta, upper, lower, "B12"

    raise Exception(
        f"ERROR           | Logic error. color=({red}, {green}, {blue})")


def to_color_rate(vertical_parcent, theta):
    """
    vertical_parcent : [float, float, float]
        合計 1.0 となる 0.0～1.0 の値が３つ。
        箱の１段目、２段目、３段目の順
    theta : float
        弧度法。0°を １２時の方向（赤）とし、
        時計回りに黄色、緑、青緑……、と進んでいきます
    """

    # 円周上の３点のx位置
    r_x = math.cos(math.radians(theta))
    g_x = math.cos(math.radians(theta-120))
    b_x = math.cos(math.radians(theta+120))

    # -1.0 ～ 1.0 を使いやすいように 0.0 ～ 1.0 に変換
    rrx = (r_x + 1.0) / 2
    ggx = (g_x + 1.0) / 2
    bbx = (b_x + 1.0) / 2

    right_end = max(rrx, ggx, bbx)
    left_end = min(rrx, ggx, bbx)
    diff = right_end - left_end

    rrrx = __one_fit(rrx, left_end, diff)
    gggx = __one_fit(ggx, left_end, diff)
    bbbx = __one_fit(bbx, left_end, diff)

    # 'vertical_parcent[1]' - 箱全体に占める２段目の箱の縦幅の割合 0.0～1.0
    # 'vertical_parcent[2]' - 箱全体に占める３段目の箱の縦幅の割合 0.0～1.0
    # 0.0 ～ 1.0 の比で返します
    return (
        rrrx * vertical_parcent[1] + vertical_parcent[2],
        gggx * vertical_parcent[1] + vertical_parcent[2],
        bbbx * vertical_parcent[1] + vertical_parcent[2])


def __one_fit(rate, left_end, diff):
    """フィットさせます"""
    if diff == 0:
        return 0  # 0除算が起こるなら（仕方が無いので）差分は 0 にします
    return (rate-left_end) / diff
