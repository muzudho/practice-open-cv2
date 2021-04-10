"""HULモデル
ソースコードはGPLが混じってるが、HULモデル自体はアルゴリズムなんで著作権は無いぜ（＾～＾）

HSVモデルの仲間で、
色相と色調を扱うライブラリの実装です。
"""

import math


ACCURACY = 0.0000001  # 浮動小数点精度


def round_limit(number):
    """0.34999999999999 みたいな数を 0.35 にし、
    0.35000000000002 みたいな数を 0.35 にする操作。
    この関数によって、精度は下がってしまいます。
    これで丸めを取ってもまた丸まっていることもある気もする。
    """
    accuracy = 10000000000  # こんなん適当な桁（＾～＾）上手く行くとしたらまぐれ（＾～＾）
    num1 = math.floor(number*accuracy)
    num2 = math.floor(number*accuracy+1)
    num3 = math.floor(num1 / (accuracy/100))
    num4 = math.floor(num2/(accuracy/100))
    if num4 - num3 < 1:
        # 極限を切り捨てます
        return num1 / accuracy
    # 極限を切り上げます
    new_number = num2 / accuracy
    return new_number


def inverse_func_degrees(color):
    """逆関数。精度は int型の弧度法しかありません"""
    theta, upper, lower, c_phase = inverse_func(color)

    if c_phase in ('A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'B1u', 'B3d', 'B9u'):
        angle = round_limit(math.degrees(theta))
    elif c_phase in ('B1', 'B3', 'B5', 'B7', 'B7d', 'B9', 'B11', 'B11d'):
        angle = math.floor(math.degrees(theta))
    elif c_phase in ('B2', 'B4', 'B5u', 'B6', 'B8', 'B10', 'B12'):
        angle = math.ceil(math.degrees(theta))
    else:
        raise Exception(
            f"ERROR           | Logic error. theta={theta} upper={upper} \
lower={lower} c_phase={c_phase}")

    return angle, upper, lower, c_phase


def inverse_func(color):
    """逆関数。ラジアン値で 0.02 未満の誤差が出ます"""
    c_phase = color_phase(color)
    # 一応、浮動小数点数の丸め誤差を消しとくか。厳密じゃないけど（＾～＾）
    red = round_limit(color[0])
    green = round_limit(color[1])
    blue = round_limit(color[2])
    if c_phase == 'M':
        raise Exception(f"monocro color=({red}, {green}, {blue})")

    upper = max(red, green, blue)
    lower = min(red, green, blue)

    if c_phase == 'A1':
        return math.radians(0), upper, lower, c_phase
    if c_phase == 'A2':
        return math.radians(60), upper, lower, c_phase
    if c_phase == 'A3':
        return math.radians(120), upper, lower, c_phase
    if c_phase == 'A4':
        return math.radians(180), upper, lower, c_phase
    if c_phase == 'A5':
        return math.radians(240), upper, lower, c_phase
    if c_phase == 'A6':
        return math.radians(300), upper, lower, c_phase

    # 1本はU、1本はL なので、U と L を消せば動いているバーの長さになります
    bar_length = red + green + blue - upper - lower
    width = round_limit(bar_length - lower)

    diameter = upper - lower

    if c_phase in ('B1', 'B1u'):
        # パターン１ (0°～30°)
        theta = math.asin(width/diameter)
    elif c_phase == 'B2':
        # パターン２
        theta = math.acos((diameter-width)/diameter) - math.radians(30)
    elif c_phase in ('B3', 'B3d'):
        # パターン３
        theta = math.asin((diameter - width)/diameter) + math.radians(60)
    elif c_phase == 'B4':
        # パターン４ (赤バーが下半分で減っていっている)
        theta = math.acos(width/diameter) + math.radians(30)
    elif c_phase in ('B5', 'B5u'):
        # パターン５
        theta = math.asin(width/diameter) + math.radians(120)
    elif c_phase == 'B6':
        # パターン６
        theta = math.acos((diameter - width)/diameter) + math.radians(90)
    elif c_phase in ('B7', 'B7d'):
        # パターン７
        theta = math.asin((diameter - width)/diameter) + math.radians(180)
    elif c_phase == 'B8':
        # パターン８
        theta = math.acos(width/diameter) + math.radians(150)
    elif c_phase in ('B9', 'B9u'):
        # パターン９
        theta = math.asin(width/diameter) + math.radians(240)
    elif c_phase == 'B10':
        # パターン１０
        theta = math.acos((diameter - width)/diameter) + math.radians(210)
    elif c_phase in ('B11', 'B11d'):
        # パターン１１
        theta = math.asin((diameter - width)/diameter) + math.radians(300)
    elif c_phase == 'B12':
        # パターン１２
        theta = math.acos(width/diameter) + math.radians(270)
    else:
        raise Exception(
            f"ERROR           | Logic error. color=({red}, {green}, {blue})")

    return theta, upper, lower, c_phase


def color_phase(color):
    """角度を M、A1～A6、B1～B12, B1u, B3d, B5u, B7d, B9u, B11d の文字列で返します"""

    # 浮動小数点数の丸め誤差を消さないと等号比較ができないぜ（＾～＾）
    red = round_limit(color[0])
    green = round_limit(color[1])
    blue = round_limit(color[2])
    if math.isclose(red, green, abs_tol=ACCURACY) \
            and math.isclose(green, blue, abs_tol=ACCURACY):
        # Monocro
        return 'M'

    upper = max(red, green, blue)
    lower = min(red, green, blue)

    if math.isclose(green, blue, abs_tol=ACCURACY) and math.isclose(red, upper, abs_tol=ACCURACY):
        c_phase = "A1"
    elif math.isclose(red, green, abs_tol=ACCURACY) and math.isclose(blue, lower, abs_tol=ACCURACY):
        c_phase = "A2"
    elif math.isclose(red, blue, abs_tol=ACCURACY) and math.isclose(green, upper, abs_tol=ACCURACY):
        c_phase = "A3"
    elif math.isclose(green, blue, abs_tol=ACCURACY) and math.isclose(red, lower, abs_tol=ACCURACY):
        c_phase = "A4"
    elif math.isclose(red, green, abs_tol=ACCURACY) and math.isclose(blue, upper, abs_tol=ACCURACY):
        c_phase = "A5"
    elif math.isclose(red, blue, abs_tol=ACCURACY) and math.isclose(green, lower, abs_tol=ACCURACY):
        c_phase = "A6"
    else:
        c_phase = None

    if c_phase is not None:
        return c_phase

    # 1本はU、1本はL なので、U と L を消せば動いているバーの長さになります
    bar_length = red + green + blue - upper - lower
    width = round_limit(bar_length - lower)

    diameter = upper - lower
    radius = round_limit(diameter / 2)

    if math.isclose(red, upper, abs_tol=ACCURACY) \
            and not math.isclose(green, upper, abs_tol=ACCURACY) \
            and math.isclose(blue, lower, abs_tol=ACCURACY):
        # 緑上昇中
        if math.isclose(width, radius, abs_tol=ACCURACY):
            # +-+
            # | |
            # | |  +-+      x == 30°
            # | |  | |
            # +-+  +-+  +-+
            #  R    G    B
            c_phase = 'B1u'
        # パターン１
        elif width < radius:
            # +-+
            # | |
            # | |  +-+              < 30°
            # | |  |^|            x
            # +-+  +-+  +-+ 0° <=
            #  R    G    B
            c_phase = 'B1'
        # パターン２
        else:
            # +-+                   < 60°
            # | |   ^             x
            # | |  +-+      30° <
            # | |  | |
            # +-+  +-+  +-+
            #  R    G    B
            c_phase = 'B2'
    elif not math.isclose(red, lower, abs_tol=ACCURACY) \
            and math.isclose(green, upper, abs_tol=ACCURACY) \
            and math.isclose(blue, lower, abs_tol=ACCURACY):
        # 赤下降中
        if math.isclose(width, radius, abs_tol=ACCURACY):
            #      +-+
            #      | |
            # +-+  | |      x == 90°
            # | |  | |
            # +-+  +-+  +-+
            #  R    G    B
            c_phase = 'B3d'
        # パターン３
        elif radius < width:
            #      +-+               < 120°
            #  v   | |             x
            # +-+  | |      90° <=
            # | |  | |
            # +-+  +-+  +-+
            #  R    G    B
            c_phase = 'B3'
        # パターン４
        else:
            #      +-+
            #      | |
            # +-+  | |               < 90°
            # |v|  | |             x
            # +-+  +-+  +-+ 60° <=
            #  R    G    B
            c_phase = 'B4'
    elif math.isclose(red, lower, abs_tol=ACCURACY) \
            and math.isclose(green, upper, abs_tol=ACCURACY) \
            and not math.isclose(blue, upper, abs_tol=ACCURACY):
        # 青上昇中
        if math.isclose(width, radius, abs_tol=ACCURACY):
            #      +-+
            #      | |
            #      | |  +-+ x == 150°
            #      | |  | |
            # +-+  +-+  +-+
            #  R    G    B
            c_phase = 'B5u'
        # パターン５
        elif width < radius:  # 半分を含まない（必要）
            #      +-+
            #      | |
            #      | |  +-+           < 150°
            #      | |  |^|         x
            # +-+  +-+  +-+ 120° <=
            #  R    G    B
            c_phase = 'B5'
        # パターン６
        else:
            #      +-+                < 180°
            #      | |   ^          x
            #      | |  +-+ 150° <=
            #      | |  | |
            # +-+  +-+  +-+
            #  R    G    B
            c_phase = 'B6'
    elif math.isclose(red, lower, abs_tol=ACCURACY) \
            and not math.isclose(green, lower, abs_tol=ACCURACY) \
            and math.isclose(blue, upper, abs_tol=ACCURACY):
        # 緑下降中
        # パターン７
        if math.isclose(width, radius, abs_tol=ACCURACY):
            #      +-+
            #      | |
            #      | |  +-+ x == 210°
            #      | |  | |
            # +-+  +-+  +-+
            #  R    G    B
            c_phase = 'B7d'
        elif radius < width:
            #           +-+          < 180°
            #       v   | |        x
            #      +-+  | | 210° <
            #      | |  | |
            # +-+  +-+  +-+
            #  R    G    B
            c_phase = 'B7'
        # パターン８
        else:
            #           +-+
            #           | |
            #      +-+  | |          < 210°
            #      |v|  | |        x
            # +-+  +-+  +-+ 240° <
            #  R    G    B
            c_phase = 'B8'
    elif not math.isclose(red, upper, abs_tol=ACCURACY) \
            and math.isclose(green, lower, abs_tol=ACCURACY) \
        and math.isclose(blue, upper, abs_tol=ACCURACY):
        # 赤上昇中
        if math.isclose(width, radius, abs_tol=ACCURACY):
            #           +-+
            #           | |
            # +-+       | | x == 270°
            # | |       | |
            # +-+  +-+  +-+
            #  R    G    B
            c_phase = 'B9u'
        # パターン９
        elif width < radius:
            #           +-+
            #           | |
            # +-+       | |           < 270°
            # |^|       | |         x
            # +-+  +-+  +-+ 240° <=
            #  R    G    B
            c_phase = 'B9'
        # パターン１０
        else:
            #           +-+          < 300°
            #  ^        | |        x
            # +-+       | | 270° <
            # | |       | |
            # +-+  +-+  +-+
            #  R    G    B
            c_phase = 'B10'
    elif math.isclose(red, upper, abs_tol=ACCURACY) \
            and math.isclose(green, lower, abs_tol=ACCURACY) \
            and not math.isclose(blue, lower, abs_tol=ACCURACY):
        # 青下降中
        if math.isclose(width, radius, abs_tol=ACCURACY):
            #           +-+
            #           | |
            # +-+       | | x == 330°
            # | |       | |
            # +-+  +-+  +-+
            #  R    G    B
            c_phase = 'B11d'
        # パターン１１
        elif radius < width:
            # +-+           300° <
            # | |        v         x
            # | |       +-+          < 330°
            # | |       | |
            # +-+  +-+  +-+
            #  R    G    B
            c_phase = 'B11'
        # パターン１２
        else:
            # +-+
            # | |
            # | |       +-+ 330° <
            # | |       |v|        x
            # +-+  +-+  +-+          < 360°
            #  R    G    B
            c_phase = 'B12'
    else:
        raise Exception(
            f"ERROR           | Logic error. color=({red}, {green}, {blue})")

    return c_phase


def to_color_rate(vertical_parcent, theta):
    """
    vertical_parcent : [float, float, float]
        合計 1.0 となる 0.0～1.0 の値が３つ。
        箱の１段目、２段目、３段目の順
    theta : float
        ラジアンで 0 を １２時の方向（赤）とし、
        時計回りに黄色、緑、青緑……、と進んでいきます
    """

    # 円周上の３点のx位置
    r_x = math.cos(theta)
    g_x = math.cos(theta-math.radians(120))
    b_x = math.cos(theta+math.radians(120))

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
        return 0.0  # 0除算が起こるなら（仕方が無いので）差分は 0 にします
    return (rate-left_end) / diff
