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

    # 1本はU、1本はL なので、U と L を消せば動いているバーの長さになります
    bar_length = red + green + blue - upper - lower
    width = bar_length - lower

    diameter = upper - lower
    radius = diameter / 2
    adjacent = radius
    opposite = (math.sqrt(3)/2) * (diameter - width - radius)
    hipotenuse = math.sqrt(adjacent**2 + opposite**2)
    print(
        f"up={upper} low={lower} dia={diameter} rad={radius} adj={adjacent} \
red={red:4.2f} green={green:4.2f} blue={blue:4.2f} bar_length={bar_length:4.2f} width={width:4.2f} \
oppo={opposite:5.2f} hipo={hipotenuse:4.2f}")

    if red == upper and blue == lower:
        # パターン１ (0°～30°)
        if width <= diameter/2:  # 半分を含む
            theta = math.degrees(math.asin(width/diameter))
            # theta = 90 - math.degrees(math.acos(width/diameter))
            return math.floor(theta), upper, lower, "B1"
        # パターン２ (30°～60°)
        # theta = 30 - math.degrees(math.asin((diameter - width)/diameter)) + 30
        theta = math.degrees(math.acos((diameter-width)/diameter)) - 30
        return math.ceil(theta), upper, lower, "B2"
    if green == upper and blue == lower:
        # パターン３
        if diameter/2 < width:  # 半分を含まない
            theta = math.degrees(math.asin((diameter - width)/diameter)) + 60
            # theta = 150 - math.degrees(math.acos((diameter - width)/diameter))
            return math.floor(theta), upper, lower, "B3"
        # パターン４ (赤バーが下半分で減っていっている)
        # theta = 30 - math.degrees(math.asin(width/diameter)) + 90
        theta = math.degrees(math.acos(width/diameter)) + 30
        return math.ceil(theta), upper, lower, "B4"
    if red == lower and green == upper:
        # パターン５
        if width <= diameter/2:  # 半分を含む
            theta = math.degrees(math.asin(width/diameter)) + 120
            return math.floor(theta), upper, lower, "B5"
        # パターン６
        # theta = 30 - \
        #    math.degrees(math.asin((diameter - width)/diameter)) + 150
        theta = math.degrees(math.acos((diameter - width)/diameter)) + 90
        return math.ceil(theta), upper, lower, "B6"
    if red == lower and blue == upper:
        if diameter/2 < width:  # 半分を含まない
            if not 0.5 < width <= 1.0:
                raise Exception(f"up={upper} low={lower} dia={diameter} rad={radius} \
adj={adjacent} red={red:4.2f} green={green:4.2f} blue={blue:4.2f} bar_length={bar_length:4.2f} \
width={width:4.2f} oppo={opposite:5.2f} hipo={hipotenuse:4.2f}")

            # パターン７
            # theta = math.degrees(math.asin((diameter - width)/diameter)) + 180
            #
            opposite = (math.sqrt(3)/2) * (radius - width)
            hipotenuse = math.sqrt(adjacent**2 + opposite**2)
            rad = opposite / hipotenuse
            print(f"oppo={opposite:5.2f} hipo={hipotenuse:5.2f} rad={rad:5.2f}")
            theta = math.degrees(math.atan(rad)) + 60
            return theta, upper, lower, "B7"
            # return math.floor(theta), upper, lower, "B7"
        # パターン８
        #opposite = (math.sqrt(3)/2) * (diameter - width - radius)
        #adjacent = 1
        #hipotenuse = math.sqrt(adjacent**2 + opposite**2)
        #theta = math.degrees(math.atan(opposite / hipotenuse)) + 150
        #
        # theta = 30 - math.degrees(math.asin(width/diameter)) + 210
        theta = math.degrees(math.acos(width/diameter)) + 150
        #
        # theta = math.degrees(math.asin(opposite / hipotenuse)) + 90
        # theta = math.degrees(math.atan(opposite / hipotenuse))
        # theta = math.degrees(math.atan(width / hipotenuse))
        # theta = math.degrees(math.acos(opposite / hipotenuse))
        return math.ceil(theta), upper, lower, "B8"
    if green == lower and blue == upper:
        # パターン９
        if width <= diameter/2:  # 半分を含む
            theta = math.degrees(math.asin(width/diameter)) + 240
            return math.floor(theta), upper, lower, "B9"
        # パターン１０
        # theta = 30 - \
        #    math.degrees(math.asin((diameter - width)/diameter)) + 270
        theta = math.degrees(math.acos((diameter - width)/diameter)) + 210
        return math.ceil(theta), upper, lower, "B10"
    if red == upper and green == lower:
        # パターン１１
        if diameter/2 < width:  # 半分を含まない
            theta = math.degrees(math.asin((diameter - width)/diameter)) + 300
            return math.floor(theta), upper, lower, "B11"
        # パターン１２
        # theta = 30 - math.degrees(math.asin(width/diameter)) + 330
        theta = math.degrees(math.acos(width/diameter)) + 270
        return math.ceil(theta), upper, lower, "B12"

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
