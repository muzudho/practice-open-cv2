"""HULモデル
ソースコードはGPLが混じってるが、HULモデル自体はアルゴリズムなんで著作権は無いぜ（＾～＾）

HSVモデルの仲間で、
色相と色調を扱うライブラリの実装です。
"""

import math


ACCURACY = 0.0000001  # 浮動小数点精度


def inverse_func_degrees(color):
    """逆関数。精度は int型の弧度法しかありません"""
    theta, upper, lower, c_phase = inverse_func(color)

    # 切り上げ、切り捨てで、ずれを微調整
    if c_phase == 'M':
        angle = float('Nan')
    elif c_phase in ('A1', 'A2', 'A3', 'A4', 'A5', 'A6',
                     'B1u', 'B3d', 'B5u', 'B7d', 'B9u', 'B11d'):  # キリがいい数
        angle = math.degrees(theta)
    # 'C1u', 'C3d', 'C5u', 'C7d', 'C9u', 'C11d' は diff が正の数なので、そのまま切り捨てでいい。
    elif c_phase in ('C1u', 'C3d', 'C5u', 'C7d', 'C9u', 'C11d'):  # 奇数
        angle = math.floor(math.degrees(theta))
        # angle = math.degrees(theta)
    # 'C2u', 'C4d', 'C6u', 'C8d', 'C10u', 'C12d' はdiffが負の数なので、 ceil すると 切り捨ての効果が出る。
    elif c_phase in ('C2u', 'C4d', 'C6u', 'C8d', 'C10u', 'C12d'):
        angle = math.ceil(math.degrees(theta))
        # angle = math.degrees(theta)
    else:
        raise Exception(
            f"ERROR           | Logic error. theta={theta} upper={upper} \
lower={lower} c_phase={c_phase}")

    return angle, upper, lower, c_phase


def inverse_func(color):
    """逆関数。ラジアン値で 0.02 未満の誤差が出ます。
    モノクロのとき Nan を返します"""
    c_phase = color_phase(color)
    # 一応、浮動小数点数の丸め誤差を消しとくか。厳密じゃないけど（＾～＾）
    red = color[0]
    green = color[1]
    blue = color[2]
    if c_phase == 'M':
        return float('Nan')
        # raise Exception(f"monocro color=({red}, {green}, {blue})")

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
    width = bar_length - lower

    diameter = upper - lower
    #radius = diameter/2
    #adjacent = radius
    #tanjent = diameter - width - radius
    #opposite = (math.sqrt(3)/2) * tanjent
    #hipotenuse = math.sqrt(adjacent**2 + opposite**2)

    # B?up は asin, C奇数? も asin
    # B?down は acos, C偶数? も acos
    if c_phase in ('C1u', 'B1u'):
        # パターン１ (0°～30°)
        theta = math.asin(width/diameter)
    elif c_phase == 'C2u':
        # パターン２
        theta = math.acos((diameter-width)/diameter) - math.radians(30)
    elif c_phase == ('C3d'):
        # パターン３
        theta = math.asin((diameter - width)/diameter) + math.radians(60)
    elif c_phase in ('B3d', 'C4d'):
        # パターン４ (赤バーが下半分で減っていっている)
        theta = math.acos(width/diameter) + math.radians(30)
    elif c_phase in ('C5u', 'B5u'):
        # パターン５
        theta = math.asin(width/diameter) + math.radians(120)
    elif c_phase == 'C6u':
        # パターン６
        theta = math.acos((diameter - width)/diameter) + math.radians(90)
    elif c_phase in ('C7d', 'B7d'):
        # パターン７
        theta = math.asin((diameter - width)/diameter) + math.radians(180)
    elif c_phase == 'C8d':
        # パターン８
        theta = math.acos(width/diameter) + math.radians(150)
    elif c_phase in ('C9u', 'B9u'):
        # パターン９
        theta = math.asin(width/diameter) + math.radians(240)
    elif c_phase == 'C10u':
        # パターン１０
        theta = math.acos((diameter - width)/diameter) + math.radians(210)
    elif c_phase == ('C11d'):
        # パターン１１
        theta = math.asin((diameter - width)/diameter) + math.radians(300)
    elif c_phase in ('B11d', 'C12d'):
        # パターン１２
        theta = math.acos(width/diameter) + math.radians(270)
    else:
        raise Exception(
            f"ERROR           | Logic error. color=({red}, {green}, {blue})")

    return theta, upper, lower, c_phase


def color_phase(color):
    """角度を、以下の文字列で返します。

    * 'M' - モノクロ

    A系 60°ずつ回転した形
    B系 RGBの位置関係から、１２パターンあります
    Bxu, Bxd系 １２パターンの真ん中

    * 'A1'   - (       0°     ) 緑と青は等しく、それより赤が大きい
    * 'C1u'  - (  0°<   x< 30°) 下から青、緑、赤。緑上昇中
    * 'B1u'  - (      30°     ) 下から青、緑、赤。緑上昇中
    * 'C2u'  - ( 30°<   x< 60°) 下から青、緑、赤。緑上昇中
    * 'A2'   - (      60°     ) 赤と緑は等しく、それより青は小さい
    * 'C3d'  - ( 60°<   x< 90°) 下から青、赤、緑。赤下降中
    * 'B3d'  - (      90°     ) 下から青、赤、緑。赤下降中
    * 'C4d'  - ( 90°<   x<120°) 下から青、赤、緑。赤下降中
    * 'A3'   - (     120°     ) 青と赤は等しく、それより緑が大きい
    * 'C5u'  - (120°<   x<150°) 下から赤、青、緑。青上昇中
    * 'B5u'  - (     150°     ) 下から赤、青、緑。青上昇中
    * 'C6u'  - (150°<   x<180°) 下から赤、青、緑。青上昇中
    * 'A4'   - (     180°     ) 緑と青は等しく、それより赤は小さい
    * 'C7d'  - (180°<   x<210°) 下から赤、緑、青。緑下降中
    * 'B7d'  - (     210°     ) 下から赤、緑、青。緑下降中
    * 'C8d'  - (210°<   x<240°) 下から赤、緑、青。緑下降中
    * 'A5'   - (     240°     ) 赤と緑は等しく、それより青が大きい
    * 'C9u'  - (240°<   x<270°) 下から緑、赤、青。赤上昇中
    * 'B9u'  - (     270°     ) 下から緑、赤、青。赤上昇中
    * 'C10u' - (270°<   x<300°) 下から緑、赤、青。赤上昇中
    * 'A6'   - (     300°     ) 赤と青は等しく、それより緑が小さい
    * 'C11d' - (300°<   x<330°) 下から緑、青、赤。青下降中
    * 'B11d' - (     330°     ) 下から緑、青、赤。青下降中
    * 'C12d' - (330°<   x<360°) 下から緑、青、赤。青下降中
    """

    # 浮動小数点数の丸め誤差を消さないと等号比較ができないぜ（＾～＾）
    red = color[0]
    green = color[1]
    blue = color[2]
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
    width = bar_length - lower

    diameter = upper - lower
    radius = diameter / 2

    if math.isclose(red, upper, abs_tol=ACCURACY) \
            and not math.isclose(green, upper, abs_tol=ACCURACY) \
            and math.isclose(blue, lower, abs_tol=ACCURACY):
        # 下から青、緑、赤。緑上昇中
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
            c_phase = 'C1u'
        # パターン２
        else:
            # +-+                   < 60°
            # | |   ^             x
            # | |  +-+      30° <
            # | |  | |
            # +-+  +-+  +-+
            #  R    G    B
            c_phase = 'C2u'
    elif not math.isclose(red, lower, abs_tol=ACCURACY) \
            and math.isclose(green, upper, abs_tol=ACCURACY) \
            and math.isclose(blue, lower, abs_tol=ACCURACY):
        # 下から青、赤、緑。赤下降中
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
            c_phase = 'C3d'
        # パターン４
        else:
            #      +-+
            #      | |
            # +-+  | |               < 90°
            # |v|  | |             x
            # +-+  +-+  +-+ 60° <=
            #  R    G    B
            c_phase = 'C4d'
    elif math.isclose(red, lower, abs_tol=ACCURACY) \
            and math.isclose(green, upper, abs_tol=ACCURACY) \
            and not math.isclose(blue, upper, abs_tol=ACCURACY):
        # 下から赤、青、緑。青上昇中
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
            c_phase = 'C5u'
        # パターン６
        else:
            #      +-+                < 180°
            #      | |   ^          x
            #      | |  +-+ 150° <=
            #      | |  | |
            # +-+  +-+  +-+
            #  R    G    B
            c_phase = 'C6u'
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
            c_phase = 'C7d'
        # パターン８
        else:
            #           +-+
            #           | |
            #      +-+  | |          < 210°
            #      |v|  | |        x
            # +-+  +-+  +-+ 240° <
            #  R    G    B
            c_phase = 'C8d'
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
            c_phase = 'C9u'
        # パターン１０
        else:
            #           +-+          < 300°
            #  ^        | |        x
            # +-+       | | 270° <
            # | |       | |
            # +-+  +-+  +-+
            #  R    G    B
            c_phase = 'C10u'
    elif math.isclose(red, upper, abs_tol=ACCURACY) \
            and math.isclose(green, lower, abs_tol=ACCURACY) \
            and not math.isclose(blue, lower, abs_tol=ACCURACY):
        # 青下降中
        if math.isclose(width, radius, abs_tol=ACCURACY):
            # +-+
            # | |
            # | |       +-+ x == 330°
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
            c_phase = 'C11d'
        # パターン１２
        else:
            # +-+
            # | |
            # | |       +-+ 330° <
            # | |       |v|        x
            # +-+  +-+  +-+          < 360°
            #  R    G    B
            c_phase = 'C12d'
    else:
        raise Exception(
            f"ERROR           | Logic error. color=({red}, {green}, {blue})")

    return c_phase


def to_color_rate(bar_rate, theta):
    """
    bar_rate : [float, float, float]
        合計 1.0 となる 0.0～1.0 の値が３つ。
        左の箱から１、２、３番目の順
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

    return (
        rrrx * bar_rate[1] + bar_rate[0],
        gggx * bar_rate[1] + bar_rate[0],
        bbbx * bar_rate[1] + bar_rate[0])


def __one_fit(rate, left_end, diff):
    """フィットさせます"""
    if diff == 0:
        return 0.0  # 0除算が起こるなら（仕方が無いので）差分は 0 にします
    return (rate-left_end) / diff
