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
    elif c_phase in ('A00u', 'A04D', 'A08u', 'A12D', 'A16u', 'A20D',
                     'C02u', 'C06D', 'C10u', 'C14D', 'C18u', 'C22D'):  # キリがいい数
        angle = math.degrees(theta)
    # 'B01u', 'B05D', 'B09u', 'B13D', 'B17u', 'B21D' は diff が正の数なので、そのまま切り捨てでいい。
    elif c_phase in ('B01u', 'B05D', 'B09u', 'B13D', 'B17u', 'B21D'):  # 奇数
        angle = math.floor(math.degrees(theta))
        # angle = math.degrees(theta)
    # 'D03U', 'D07d', 'D11U', 'D15d', 'D19U', 'D23d' はdiffが負の数なので、 ceil すると 切り捨ての効果が出る。
    elif c_phase in ('D03U', 'D07d', 'D11U', 'D15d', 'D19U', 'D23d'):
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

    if c_phase == 'A00u':
        theta = math.radians(0)
    elif c_phase == 'C02u':
        theta = math.radians(30)
    elif c_phase == 'A04D':
        theta = math.radians(60)
    elif c_phase == 'C06D':
        theta = math.radians(90)
    elif c_phase == 'A08u':
        theta = math.radians(120)
    elif c_phase == 'C10u':
        theta = math.radians(150)
    elif c_phase == 'A12D':
        theta = math.radians(180)
    elif c_phase == 'C14D':
        theta = math.radians(210)
    elif c_phase == 'A16u':
        theta = math.radians(240)
    elif c_phase == 'C18u':
        theta = math.radians(270)
    elif c_phase == 'A20D':
        theta = math.radians(300)
    elif c_phase == 'C22D':
        theta = math.radians(330)
    else:
        theta = None

    if theta is not None:
        return theta, upper, lower, c_phase

    # 1本はU、1本はL なので、U と L を消せば動いているバーの長さになります
    bar_length = red + green + blue - upper - lower
    width = bar_length - lower

    diameter = upper - lower
    #radius = diameter/2
    #adjacent = radius
    #tanjent = diameter - width - radius
    #opposite = (math.sqrt(3)/2) * tanjent
    #hipotenuse = math.sqrt(adjacent**2 + opposite**2)

    # asin - B数u, B数D
    # acos - D数U, D数d
    # 全部 asin にする、とかやりたいが、切り上げ、切り捨て、丸め で合わないので、仕方なく分けてあるぜ（＾～＾）
    if c_phase == 'B01u':
        # パターン１ (widthは半径よりは短い)
        theta = math.asin(width/diameter)
    elif c_phase == 'D03U':
        # パターン２ (widthは半径よりは長い)
        theta = math.acos((diameter - width)/diameter) - math.radians(30)
    elif c_phase == 'B05D':
        # パターン３ (widthは半径よりは長い)
        theta = math.asin((diameter - width)/diameter) + math.radians(60)
    elif c_phase == 'D07d':
        # パターン４ (widthは半径よりは短い)
        theta = math.acos(width/diameter) + math.radians(30)
    elif c_phase == 'B09u':
        # パターン５ (widthは半径よりは短い)
        theta = math.asin(width/diameter) + math.radians(120)
    elif c_phase == 'D11U':
        # パターン６ (widthは半径よりは長い)
        theta = math.acos((diameter - width)/diameter) + math.radians(90)
    elif c_phase == 'B13D':
        # パターン７ (widthは半径よりは長い)
        theta = math.asin((diameter - width)/diameter) + math.radians(180)
    elif c_phase == 'D15d':
        # パターン８ (widthは半径よりは短い)
        theta = math.acos(width/diameter) + math.radians(150)
    elif c_phase == 'B17u':
        # パターン９ (widthは半径よりは短い)
        theta = math.asin(width/diameter) + math.radians(240)
    elif c_phase == 'D19U':
        # パターン１０ (widthは半径よりは長い)
        theta = math.acos((diameter - width)/diameter) + math.radians(210)
    elif c_phase == 'B21D':
        # パターン１１ (widthは半径よりは長い)
        theta = math.asin((diameter - width)/diameter) + math.radians(300)
    elif c_phase == 'D23d':
        # パターン１２ (widthは半径よりは短い)
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

    * 'A00u' - (       0°     ) 緑と青は等しく、それより赤が大きい
    * 'B01u' - (  0°<   x< 30°) 下から青、緑、赤。緑上昇中
    * 'C02u' - (      30°     ) 下から青、緑、赤。緑上昇中
    * 'D03U' - ( 30°<   x< 60°) 下から青、緑、赤。緑上昇中
    * 'A04D' - (      60°     ) 赤と緑は等しく、それより青は小さい
    * 'B05D' - ( 60°<   x< 90°) 下から青、赤、緑。赤下降中
    * 'C06D' - (      90°     ) 下から青、赤、緑。赤下降中
    * 'D07d' - ( 90°<   x<120°) 下から青、赤、緑。赤下降中
    * 'A08u' - (     120°     ) 青と赤は等しく、それより緑が大きい
    * 'B09u' - (120°<   x<150°) 下から赤、青、緑。青上昇中
    * 'C10u' - (     150°     ) 下から赤、青、緑。青上昇中
    * 'D11U' - (150°<   x<180°) 下から赤、青、緑。青上昇中
    * 'A12D' - (     180°     ) 緑と青は等しく、それより赤は小さい
    * 'B13D' - (180°<   x<210°) 下から赤、緑、青。緑下降中
    * 'C14D' - (     210°     ) 下から赤、緑、青。緑下降中
    * 'D15d' - (210°<   x<240°) 下から赤、緑、青。緑下降中
    * 'A16u' - (     240°     ) 赤と緑は等しく、それより青が大きい
    * 'B17u' - (240°<   x<270°) 下から緑、赤、青。赤上昇中
    * 'C18u' - (     270°     ) 下から緑、赤、青。赤上昇中
    * 'D19U' - (270°<   x<300°) 下から緑、赤、青。赤上昇中
    * 'A20D' - (     300°     ) 赤と青は等しく、それより緑が小さい
    * 'B21D' - (300°<   x<330°) 下から緑、青、赤。青下降中
    * 'C22D' - (     330°     ) 下から緑、青、赤。青下降中
    * 'D23d' - (330°<   x<360°) 下から緑、青、赤。青下降中
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
        c_phase = 'A00u'
    elif math.isclose(red, green, abs_tol=ACCURACY) and math.isclose(blue, lower, abs_tol=ACCURACY):
        c_phase = 'A04D'
    elif math.isclose(red, blue, abs_tol=ACCURACY) and math.isclose(green, upper, abs_tol=ACCURACY):
        c_phase = 'A08u'
    elif math.isclose(green, blue, abs_tol=ACCURACY) and math.isclose(red, lower, abs_tol=ACCURACY):
        c_phase = 'A12D'
    elif math.isclose(red, green, abs_tol=ACCURACY) and math.isclose(blue, upper, abs_tol=ACCURACY):
        c_phase = 'A16u'
    elif math.isclose(red, blue, abs_tol=ACCURACY) and math.isclose(green, lower, abs_tol=ACCURACY):
        c_phase = 'A20D'
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
            c_phase = 'C02u'
        # パターン１
        elif width < radius:
            # +-+
            # | |
            # | |  +-+              < 30°
            # | |  |^|            x
            # +-+  +-+  +-+ 0° <=
            #  R    G    B
            c_phase = 'B01u'
        # パターン２
        else:
            # +-+                   < 60°
            # | |   ^             x
            # | |  +-+      30° <
            # | |  | |
            # +-+  +-+  +-+
            #  R    G    B
            c_phase = 'D03U'
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
            c_phase = 'C06D'
        # パターン３
        elif radius < width:
            #      +-+               < 120°
            #  v   | |             x
            # +-+  | |      90° <=
            # | |  | |
            # +-+  +-+  +-+
            #  R    G    B
            c_phase = 'B05D'
        # パターン４
        else:
            #      +-+
            #      | |
            # +-+  | |               < 90°
            # |v|  | |             x
            # +-+  +-+  +-+ 60° <=
            #  R    G    B
            c_phase = 'D07d'
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
            c_phase = 'C10u'
        # パターン５
        elif width < radius:  # 半分を含まない（必要）
            #      +-+
            #      | |
            #      | |  +-+           < 150°
            #      | |  |^|         x
            # +-+  +-+  +-+ 120° <=
            #  R    G    B
            c_phase = 'B09u'
        # パターン６
        else:
            #      +-+                < 180°
            #      | |   ^          x
            #      | |  +-+ 150° <=
            #      | |  | |
            # +-+  +-+  +-+
            #  R    G    B
            c_phase = 'D11U'
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
            c_phase = 'C14D'
        elif radius < width:
            #           +-+          < 180°
            #       v   | |        x
            #      +-+  | | 210° <
            #      | |  | |
            # +-+  +-+  +-+
            #  R    G    B
            c_phase = 'B13D'
        # パターン８
        else:
            #           +-+
            #           | |
            #      +-+  | |          < 210°
            #      |v|  | |        x
            # +-+  +-+  +-+ 240° <
            #  R    G    B
            c_phase = 'D15d'
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
            c_phase = 'C18u'
        # パターン９
        elif width < radius:
            #           +-+
            #           | |
            # +-+       | |           < 270°
            # |^|       | |         x
            # +-+  +-+  +-+ 240° <=
            #  R    G    B
            c_phase = 'B17u'
        # パターン１０
        else:
            #           +-+          < 300°
            #  ^        | |        x
            # +-+       | | 270° <
            # | |       | |
            # +-+  +-+  +-+
            #  R    G    B
            c_phase = 'D19U'
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
            c_phase = 'C22D'
        # パターン１１
        elif radius < width:
            # +-+           300° <
            # | |        v         x
            # | |       +-+          < 330°
            # | |       | |
            # +-+  +-+  +-+
            #  R    G    B
            c_phase = 'B21D'
        # パターン１２
        else:
            # +-+
            # | |
            # | |       +-+ 330° <
            # | |       |v|        x
            # +-+  +-+  +-+          < 360°
            #  R    G    B
            c_phase = 'D23d'
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
