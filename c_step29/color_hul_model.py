"""HULモデル
この color_hul_model.py ファイルに GPL は混ざってないが、
リポジトリにGPLが混じっていて、そのライブラリの一部になっているから、GPLが嫌なら、厳密に言えば、
HULモデルはアルゴリズムなんで 著作権無いんで理解したら ソースを一から独自実装し直して持ってけだぜ（＾～＾）

Hue(色相環の角度、弧度法)、Upper(上限値)、Lower(下限値) から色を求めます。

HSVモデルの仲間で、
色相と色調を扱うライブラリの実装です。

to_hue_angle()関数の使い方
=========================

このプログラムで color というと、以下の仕様です。
RGB値は R, G, B の順で 0.0～1.0 で指定してください。

       Lower            Upper
 0.0    0.2              0.7      1.0
  +------+----------------+--------+
R |      |                | 0.7    |
  +------+-------+--------+        |
G |      |       | 0.4             |
  +------+-------+                 |
B |      | 0.2                     |
  +------+-------------------------+

  <-----> <--------------> <------>
   Left    Middle           Right
   Box     Box              Box

color = (0.7, 0.4, 0.2)

to_hue_angle()関数を使うと 弧度法が返ってきます。
戻り値の２つ目はデバッグ用の情報なので要りません。

hue_angle, _ = to_hue_angle(color)
# hue_angle is 23

to_color()関数の使い方
=====================

(再掲)
       Lower            Upper
 0.0    0.2              0.7      1.0
  +------+----------------+--------+
R |      |                | 0.7    |
  +------+-------+--------+        |
G |      |       | 0.4             |
  +------+-------+                 |
B |      | 0.2                     |
  +------+-------------------------+

  <-----> <--------------> <------>
   Left    Middle           Right
   Box     Box              Box

to_color()関数を使うと color が返ってきます。
第一引数のリストは先頭から、全体を 1.0 としたときの LeftBoxの比、MiddleBoxの比、RightBoxの比です。
第二引数は色相環の角度（ラジアン）です。

color = to_color([0.2, 0.5, 0.3], math.radians(23))
# color is (0.7, 0.39683272553278354, 0.2)

hul_to_color()関数の使い方
=====================

しかし、せっかく HULモデル(Hue,Upper,Lowerモデル)という名前なのですから、
Upper値、Lower値を使っても 色 を出せるようにしましょう。
引数の順番は 先頭から Hue(弧度法), Upper, Lower です。

color = hul_to_color(23, 0.7, 0.2)
# color is (0.7, 0.3968327255327835, 0.2)
"""

import math


ACCURACY = 0.0000001  # 浮動小数点精度。ネイピアの対数表の精度をリスペクトして、適当に7桁にしたんで深い意味ない（＾～＾）


def hul_to_color(hue_angle, upper, lower):
    """順関数。RGB値を 0.0～1.0 とする色を返します"""
    return to_color([lower, upper-lower, 1.0-(upper-lower)], math.radians(hue_angle))


def to_hue_angle(color):
    """逆関数。精度は int型の弧度法しかありません"""
    theta, upper, lower, c_phase = __inverse_func_radians(color)

    # 弧度法の整数部の精度で調整したので、小数部を切り上げ、切り捨てして、ずれを0にします
    # M はモノクロ
    if c_phase == 'M':
        angle = float('Nan')
    # A,C系は キリがいい数
    elif c_phase in ('A00u', 'A04D', 'A08u', 'A12D', 'A16u', 'A20D',
                     'C02U', 'C06d', 'C10U', 'C14d', 'C18U', 'C22d'):
        angle = math.degrees(theta)
    # B系は diff が正の数なので、そのまま切り捨てでいい
    elif c_phase in ('B01u', 'B05D', 'B09u', 'B13D', 'B17u', 'B21D'):
        angle = math.floor(math.degrees(theta))
    # D系 はdiffが負の数なので、 ceil すると 切り捨ての効果が出る
    elif c_phase in ('D03U', 'D07d', 'D11U', 'D15d', 'D19U', 'D23d'):
        angle = math.ceil(math.degrees(theta))
    else:
        raise Exception(
            f"ERROR           | Logic error. theta={theta} upper={upper} \
lower={lower} c_phase={c_phase}")

    return angle, (upper, lower, c_phase)


def __inverse_func_radians(color):
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
    elif c_phase == 'C02U':
        theta = math.radians(30)
    elif c_phase == 'A04D':
        theta = math.radians(60)
    elif c_phase == 'C06d':
        theta = math.radians(90)
    elif c_phase == 'A08u':
        theta = math.radians(120)
    elif c_phase == 'C10U':
        theta = math.radians(150)
    elif c_phase == 'A12D':
        theta = math.radians(180)
    elif c_phase == 'C14d':
        theta = math.radians(210)
    elif c_phase == 'A16u':
        theta = math.radians(240)
    elif c_phase == 'C18U':
        theta = math.radians(270)
    elif c_phase == 'A20D':
        theta = math.radians(300)
    elif c_phase == 'C22d':
        theta = math.radians(330)
    else:
        theta = None

    if theta is not None:
        return theta, upper, lower, c_phase

    # 1本はU、1本はL なので、U と L を消せば動いているバーの長さになります
    bar_length = red + green + blue - upper - lower
    width = bar_length - lower
    diameter = upper - lower

    # 1文字目が Bなら asin, Dなら acos です。
    # 4文字目が大文字の U,Dなら width が 半径より長く、 小文字の u,d なら width が半径より短いぜ（＾～＾）
    #
    # sin(30°)=0.5、cos(60°)=0.5 と、30°刻みの角度を有理数にできるから sin, cos の逆関数 asin, acos を使ってるだけで、
    # ラジアンで 0.02未満、弧度法で 0.7未満の誤差があるぜ（＾～＾） つまり騙し絵、フェイク画像（＾～＾）
    # ちょうどいい曲線をぶつけただけで 正確な曲線を取れてないぜ（＾～＾）
    #
    # 全部 asin にする、とか asin, acos のどちらかに揃えたかったが、切り上げ、切り捨て、丸め でずれるなど
    # 合わないので、仕方なく分けてあるぜ（＾～＾）
    if c_phase == 'B01u':
        theta = math.asin(width/diameter)
    elif c_phase == 'D03U':
        theta = math.acos((diameter - width)/diameter) - math.radians(30)
    elif c_phase == 'B05D':
        theta = math.asin((diameter - width)/diameter) + math.radians(60)
    elif c_phase == 'D07d':
        theta = math.acos(width/diameter) + math.radians(30)
    elif c_phase == 'B09u':
        theta = math.asin(width/diameter) + math.radians(120)
    elif c_phase == 'D11U':
        theta = math.acos((diameter - width)/diameter) + math.radians(90)
    elif c_phase == 'B13D':
        theta = math.asin((diameter - width)/diameter) + math.radians(180)
    elif c_phase == 'D15d':
        theta = math.acos(width/diameter) + math.radians(150)
    elif c_phase == 'B17u':
        theta = math.asin(width/diameter) + math.radians(240)
    elif c_phase == 'D19U':
        theta = math.acos((diameter - width)/diameter) + math.radians(210)
    elif c_phase == 'B21D':
        theta = math.asin((diameter - width)/diameter) + math.radians(300)
    elif c_phase == 'D23d':
        theta = math.acos(width/diameter) + math.radians(270)
    else:
        raise Exception(
            f"ERROR           | Logic error. color=({red}, {green}, {blue})")

    return theta, upper, lower, c_phase


def color_phase(color):
    """角度を、以下の文字列で返します。

    * 'M' - モノクロ

    A系  0°をスタート地点に、60°ずつ回転した形
    B系 30°の幅があるので、sin使う方
    C系 30°をスタート地点に、60°ずつ回転した形
    D系 30°の幅があるので、cos使う方

    * 'A00u' - (       0°     ) 緑と青は等しく、それより赤が大きい
    * 'B01u' - (  0°<   x< 30°) 下から青、緑、赤。緑上昇中
    * 'C02U' - (      30°     ) 下から青、緑、赤。緑上昇中
    * 'D03U' - ( 30°<   x< 60°) 下から青、緑、赤。緑上昇中
    * 'A04D' - (      60°     ) 赤と緑は等しく、それより青は小さい
    * 'B05D' - ( 60°<   x< 90°) 下から青、赤、緑。赤下降中
    * 'C06d' - (      90°     ) 下から青、赤、緑。赤下降中
    * 'D07d' - ( 90°<   x<120°) 下から青、赤、緑。赤下降中
    * 'A08u' - (     120°     ) 青と赤は等しく、それより緑が大きい
    * 'B09u' - (120°<   x<150°) 下から赤、青、緑。青上昇中
    * 'C10U' - (     150°     ) 下から赤、青、緑。青上昇中
    * 'D11U' - (150°<   x<180°) 下から赤、青、緑。青上昇中
    * 'A12D' - (     180°     ) 緑と青は等しく、それより赤は小さい
    * 'B13D' - (180°<   x<210°) 下から赤、緑、青。緑下降中
    * 'C14d' - (     210°     ) 下から赤、緑、青。緑下降中
    * 'D15d' - (210°<   x<240°) 下から赤、緑、青。緑下降中
    * 'A16u' - (     240°     ) 赤と緑は等しく、それより青が大きい
    * 'B17u' - (240°<   x<270°) 下から緑、赤、青。赤上昇中
    * 'C18U' - (     270°     ) 下から緑、赤、青。赤上昇中
    * 'D19U' - (270°<   x<300°) 下から緑、赤、青。赤上昇中
    * 'A20D' - (     300°     ) 赤と青は等しく、それより緑が小さい
    * 'B21D' - (300°<   x<330°) 下から緑、青、赤。青下降中
    * 'C22d' - (     330°     ) 下から緑、青、赤。青下降中
    * 'D23d' - (330°<   x<360°) 下から緑、青、赤。青下降中
    """

    # math.isclose()ってのは、浮動小数点数の丸め誤差を消して等号比較するやつな（＾～＾）
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
            c_phase = 'C02U'
        elif width < radius:
            # +-+
            # | |
            # | |  +-+              < 30°
            # | |  |^|            x
            # +-+  +-+  +-+ 0° <=
            #  R    G    B
            c_phase = 'B01u'
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
            c_phase = 'C06d'
        elif radius < width:
            #      +-+               < 120°
            #  v   | |             x
            # +-+  | |      90° <=
            # | |  | |
            # +-+  +-+  +-+
            #  R    G    B
            c_phase = 'B05D'
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
            c_phase = 'C10U'
        elif width < radius:  # 半分を含まない（必要）
            #      +-+
            #      | |
            #      | |  +-+           < 150°
            #      | |  |^|         x
            # +-+  +-+  +-+ 120° <=
            #  R    G    B
            c_phase = 'B09u'
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
        if math.isclose(width, radius, abs_tol=ACCURACY):
            #      +-+
            #      | |
            #      | |  +-+ x == 210°
            #      | |  | |
            # +-+  +-+  +-+
            #  R    G    B
            c_phase = 'C14d'
        elif radius < width:
            #           +-+          < 180°
            #       v   | |        x
            #      +-+  | | 210° <
            #      | |  | |
            # +-+  +-+  +-+
            #  R    G    B
            c_phase = 'B13D'
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
            c_phase = 'C18U'
        elif width < radius:
            #           +-+
            #           | |
            # +-+       | |           < 270°
            # |^|       | |         x
            # +-+  +-+  +-+ 240° <=
            #  R    G    B
            c_phase = 'B17u'
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
            c_phase = 'C22d'
        elif radius < width:
            # +-+           300° <
            # | |        v         x
            # | |       +-+          < 330°
            # | |       | |
            # +-+  +-+  +-+
            #  R    G    B
            c_phase = 'B21D'
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


def to_color(bar_rate, theta):
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


# Example:
#
#color = (0.7, 0.4, 0.2)
#hue_angle, _ = to_hue_angle(color)
#print(f"hue_angle = {hue_angle}°")
# # hue_angle = 23°
#
# color = to_color([0.2, 0.5, 0.3], math.radians(23))
# print(f"color = {color}")
# # color = (0.7, 0.39683272553278354, 0.2)
#
# color = hul_to_color(23, 0.7, 0.2)
# print(f"color = {color}")
# # color = (0.7, 0.3968327255327835, 0.2)
