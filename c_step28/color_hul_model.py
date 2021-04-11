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
    elif c_phase in ('#A___00', '#A___04', '#A___08', '#A___12', '#A___16', '#A___20',
                     '#Bu__02', '#BD__06', '#Bu__10', '#BD__14', '#Bu__18', '#BD__22'):  # キリがいい数
        angle = math.degrees(theta)
    # '#Cu__01', '#CD__05', '#Cu__09', '#CD__13', '#Cu__17', '#CD__21' は diff が正の数なので、そのまま切り捨てでいい。
    elif c_phase in ('#Cu__01', '#CD__05', '#Cu__09', '#CD__13', '#Cu__17', '#CD__21'):  # 奇数
        angle = math.floor(math.degrees(theta))
        # angle = math.degrees(theta)
    # '#CU__03', '#Cd__07', '#CU__11', '#Cd__15', '#CU__19', '#Cd__23' はdiffが負の数なので、 ceil すると 切り捨ての効果が出る。
    elif c_phase in ('#CU__03', '#Cd__07', '#CU__11', '#Cd__15', '#CU__19', '#Cd__23'):
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

    if c_phase == '#A___00':
        return math.radians(0), upper, lower, c_phase
    if c_phase == '#A___04':
        return math.radians(60), upper, lower, c_phase
    if c_phase == '#A___08':
        return math.radians(120), upper, lower, c_phase
    if c_phase == '#A___12':
        return math.radians(180), upper, lower, c_phase
    if c_phase == '#A___16':
        return math.radians(240), upper, lower, c_phase
    if c_phase == '#A___20':
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

    # asin - B数u, C奇数u, C奇数D
    # acos - B数d, C偶数U, C偶数d
    if c_phase in ('#Cu__01', '#Bu__02'):
        # パターン１ (0°～30°)
        theta = math.asin(width/diameter)
    elif c_phase == '#CU__03':
        # パターン２
        theta = math.acos((diameter-width)/diameter) - math.radians(30)
    elif c_phase == ('#CD__05'):
        # パターン３
        theta = math.asin((diameter - width)/diameter) + math.radians(60)
    elif c_phase in ('#BD__06', '#Cd__07'):
        # パターン４ (赤バーが下半分で減っていっている)
        theta = math.acos(width/diameter) + math.radians(30)
    elif c_phase in ('#Cu__09', '#Bu__10'):
        # パターン５
        theta = math.asin(width/diameter) + math.radians(120)
    elif c_phase == '#CU__11':
        # パターン６
        theta = math.acos((diameter - width)/diameter) + math.radians(90)
    elif c_phase in ('#CD__13', '#BD__14'):
        # パターン７
        theta = math.asin((diameter - width)/diameter) + math.radians(180)
    elif c_phase == '#Cd__15':
        # パターン８
        theta = math.acos(width/diameter) + math.radians(150)
    elif c_phase in ('#Cu__17', '#Bu__18'):
        # パターン９
        theta = math.asin(width/diameter) + math.radians(240)
    elif c_phase == '#CU__19':
        # パターン１０
        theta = math.acos((diameter - width)/diameter) + math.radians(210)
    elif c_phase == ('#CD__21'):
        # パターン１１
        theta = math.asin((diameter - width)/diameter) + math.radians(300)
    elif c_phase in ('#BD__22', '#Cd__23'):
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

    * '#A___00' - (       0°     ) 緑と青は等しく、それより赤が大きい
    * '#Cu__01' - (  0°<   x< 30°) 下から青、緑、赤。緑上昇中
    * '#Bu__02' - (      30°     ) 下から青、緑、赤。緑上昇中
    * '#CU__03' - ( 30°<   x< 60°) 下から青、緑、赤。緑上昇中
    * '#A___04' - (      60°     ) 赤と緑は等しく、それより青は小さい
    * '#CD__05' - ( 60°<   x< 90°) 下から青、赤、緑。赤下降中
    * '#BD__06' - (      90°     ) 下から青、赤、緑。赤下降中
    * '#Cd__07' - ( 90°<   x<120°) 下から青、赤、緑。赤下降中
    * '#A___08' - (     120°     ) 青と赤は等しく、それより緑が大きい
    * '#Cu__09' - (120°<   x<150°) 下から赤、青、緑。青上昇中
    * '#Bu__10' - (     150°     ) 下から赤、青、緑。青上昇中
    * '#CU__11' - (150°<   x<180°) 下から赤、青、緑。青上昇中
    * '#A___12' - (     180°     ) 緑と青は等しく、それより赤は小さい
    * '#CD__13' - (180°<   x<210°) 下から赤、緑、青。緑下降中
    * '#BD__14' - (     210°     ) 下から赤、緑、青。緑下降中
    * '#Cd__15' - (210°<   x<240°) 下から赤、緑、青。緑下降中
    * '#A___16' - (     240°     ) 赤と緑は等しく、それより青が大きい
    * '#Cu__17' - (240°<   x<270°) 下から緑、赤、青。赤上昇中
    * '#Bu__18' - (     270°     ) 下から緑、赤、青。赤上昇中
    * '#CU__19' - (270°<   x<300°) 下から緑、赤、青。赤上昇中
    * '#A___20' - (     300°     ) 赤と青は等しく、それより緑が小さい
    * '#CD__21' - (300°<   x<330°) 下から緑、青、赤。青下降中
    * '#BD__22' - (     330°     ) 下から緑、青、赤。青下降中
    * '#Cd__23' - (330°<   x<360°) 下から緑、青、赤。青下降中
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
        c_phase = "#A___00"
    elif math.isclose(red, green, abs_tol=ACCURACY) and math.isclose(blue, lower, abs_tol=ACCURACY):
        c_phase = "#A___04"
    elif math.isclose(red, blue, abs_tol=ACCURACY) and math.isclose(green, upper, abs_tol=ACCURACY):
        c_phase = "#A___08"
    elif math.isclose(green, blue, abs_tol=ACCURACY) and math.isclose(red, lower, abs_tol=ACCURACY):
        c_phase = "#A___12"
    elif math.isclose(red, green, abs_tol=ACCURACY) and math.isclose(blue, upper, abs_tol=ACCURACY):
        c_phase = "#A___16"
    elif math.isclose(red, blue, abs_tol=ACCURACY) and math.isclose(green, lower, abs_tol=ACCURACY):
        c_phase = "#A___20"
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
            c_phase = '#Bu__02'
        # パターン１
        elif width < radius:
            # +-+
            # | |
            # | |  +-+              < 30°
            # | |  |^|            x
            # +-+  +-+  +-+ 0° <=
            #  R    G    B
            c_phase = '#Cu__01'
        # パターン２
        else:
            # +-+                   < 60°
            # | |   ^             x
            # | |  +-+      30° <
            # | |  | |
            # +-+  +-+  +-+
            #  R    G    B
            c_phase = '#CU__03'
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
            c_phase = '#BD__06'
        # パターン３
        elif radius < width:
            #      +-+               < 120°
            #  v   | |             x
            # +-+  | |      90° <=
            # | |  | |
            # +-+  +-+  +-+
            #  R    G    B
            c_phase = '#CD__05'
        # パターン４
        else:
            #      +-+
            #      | |
            # +-+  | |               < 90°
            # |v|  | |             x
            # +-+  +-+  +-+ 60° <=
            #  R    G    B
            c_phase = '#Cd__07'
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
            c_phase = '#Bu__10'
        # パターン５
        elif width < radius:  # 半分を含まない（必要）
            #      +-+
            #      | |
            #      | |  +-+           < 150°
            #      | |  |^|         x
            # +-+  +-+  +-+ 120° <=
            #  R    G    B
            c_phase = '#Cu__09'
        # パターン６
        else:
            #      +-+                < 180°
            #      | |   ^          x
            #      | |  +-+ 150° <=
            #      | |  | |
            # +-+  +-+  +-+
            #  R    G    B
            c_phase = '#CU__11'
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
            c_phase = '#BD__14'
        elif radius < width:
            #           +-+          < 180°
            #       v   | |        x
            #      +-+  | | 210° <
            #      | |  | |
            # +-+  +-+  +-+
            #  R    G    B
            c_phase = '#CD__13'
        # パターン８
        else:
            #           +-+
            #           | |
            #      +-+  | |          < 210°
            #      |v|  | |        x
            # +-+  +-+  +-+ 240° <
            #  R    G    B
            c_phase = '#Cd__15'
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
            c_phase = '#Bu__18'
        # パターン９
        elif width < radius:
            #           +-+
            #           | |
            # +-+       | |           < 270°
            # |^|       | |         x
            # +-+  +-+  +-+ 240° <=
            #  R    G    B
            c_phase = '#Cu__17'
        # パターン１０
        else:
            #           +-+          < 300°
            #  ^        | |        x
            # +-+       | | 270° <
            # | |       | |
            # +-+  +-+  +-+
            #  R    G    B
            c_phase = '#CU__19'
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
            c_phase = '#BD__22'
        # パターン１１
        elif radius < width:
            # +-+           300° <
            # | |        v         x
            # | |       +-+          < 330°
            # | |       | |
            # +-+  +-+  +-+
            #  R    G    B
            c_phase = '#CD__21'
        # パターン１２
        else:
            # +-+
            # | |
            # | |       +-+ 330° <
            # | |       |v|        x
            # +-+  +-+  +-+          < 360°
            #  R    G    B
            c_phase = '#Cd__23'
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
