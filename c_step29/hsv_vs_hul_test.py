"""HSVモデル(円錐モデル)とHULビューの比較を行います
"""

import math
from hsv_model_hul_view import to_hue_angle as to_hul_hue_angle
from hsv_model_cone import to_hue_angle as to_hsv_cone_hue_angle
# from hsv_model_cylinder import to_hue_angle as to_hsv_cylinder_hue_angle

ACCURACY = 0.0000001  # 浮動小数点精度。ネイピアの対数表の精度をリスペクトして、適当に7桁にしたんで深い意味ない（＾～＾）

# このプログラムで color というと、以下の仕様です。
# RGB値は R, G, B の順で 0.0～1.0 で指定してください。
#        Lower            Upper
#  0.0    0.2              0.7      1.0
#   +------+----------------+--------+
# R |      |                | 0.7    |
#   +------+-------+--------+        |
# G |      |       | 0.4             |
#   +------+-------+                 |
# B |      | 0.2                     |
#   +------+-------------------------+
#
#   <-----> <--------------> <------>
#    Left    Middle           Right
#    Box     Box              Box

# 日本のHSV では、 赤180°、緑300°、青 60° です。（シアンからスタート）
# アメリカのHSV では、 赤  0°、緑120°、青240° です。（赤からスタート）
# HUL は アメリカのHSV に合わせます。

# テストケース
TEST_CASES = [
    # ３色相
    ((1.0, 0.0, 0.0), 'Vivid red'),
    ((0.0, 1.0, 0.0), 'Vivid green'),
    ((0.0, 0.0, 1.0), 'Vivid blue'),

    # ６色相
    ((1.0, 1.0, 0.0), 'Vivid yellow'),
    ((0.0, 1.0, 1.0), 'Vivid cyan'),
    ((1.0, 0.0, 1.0), 'Vivid magenta'),

    # １２色相
    ((1.0, 0.5, 0.0), 'Vivid orange'),
    ((0.5, 1.0, 0.0), 'Vivid yellow green'),
    ((0.0, 1.0, 0.5), 'Vivid blue green'),
    ((0.0, 0.5, 1.0), 'Vivid dodgers blue'),
    ((0.5, 0.0, 1.0), 'Vivid indigo'),
    ((1.0, 0.0, 0.5), 'Vivid crimson'),

    # ３６色相
    ((1.00, 0.00, 0.00), 'Vivid red'),
    ((1.00, 0.25, 0.00), 'Vivid red+'),  # B01u -１° ずれる
    ((1.00, 0.50, 0.00), 'Vivid orange'),
    ((1.00, 0.75, 0.00), 'Vivid orange+'),  # D03U +１° ずれる
    ((1.00, 1.00, 0.00), 'Vivid yellow'),
    ((0.75, 1.00, 0.00), 'Vivid yellow+'),  # B05D -1° ずれる
    ((0.50, 1.00, 0.00), 'Vivid yellow green'),
    ((0.25, 1.00, 0.00), 'Vivid yellow green+'),  # D07d +１° ずれる
    ((0.00, 1.00, 0.00), 'Vivid green'),
    ((0.00, 1.00, 0.25), 'Vivid green+'),  # B09u -１° ずれる
    ((0.00, 1.00, 0.50), 'Vivid blue green'),
    ((0.00, 1.00, 0.75), 'Vivid blue green+'),  # D11U +１° ずれる
    ((0.00, 1.00, 1.00), 'Vivid cyan'),
    ((0.00, 0.75, 1.00), 'Vivid cyan+'),   # B13D -１° ずれる
    ((0.00, 0.50, 1.00), 'Vivid dodgers blue'),
    ((0.00, 0.25, 1.00), 'Vivid dodgers blue+'),   # D15d +１° ずれる
    ((0.00, 0.00, 1.00), 'Vivid blue'),
    ((0.25, 0.00, 1.00), 'Vivid blue+'),  # B17u -１° ずれる
    ((0.50, 0.00, 1.00), 'Vivid indigo'),
    ((0.75, 0.00, 1.00), 'Vivid indigo+'),   # D19U +１° ずれる
    ((1.00, 0.00, 1.00), 'Vivid magenta'),
    ((1.00, 0.00, 0.75), 'Vivid magenta+'),   # B21D -１° ずれる
    ((1.00, 0.00, 0.50), 'Vivid crimson'),
    ((1.00, 0.00, 0.25), 'Vivid crimson+'),  # D23d +１° ずれる
]


def hsv_vs_hul_hue_angle_test(title, color):
    """HSVとHULの色相(H)が等しいかテスト
    """
    hul_hue_angle, description = to_hul_hue_angle(color)
    hsv_cone_hue_angle = to_hsv_cone_hue_angle(color)
    # hsv_cylinder_hue_angle = to_hsv_cylinder_hue_angle(color)
    # ずれたら表示します
    if not math.isclose(hul_hue_angle, hsv_cone_hue_angle, rel_tol=ACCURACY, abs_tol=ACCURACY):
            # or not math.isclose(hul_hue_angle, hsv_cylinder_hue_angle,
            #                 rel_tol = ACCURACY, abs_tol = ACCURACY):
        print(f"Angle test      | {title:22} color={color}")
        print(
            f"                | hul_hue_angle         ={hul_hue_angle:8.4f}° {description[2]}")
        print(
            f"                | hsv_cone_hue_angle    ={hsv_cone_hue_angle:8.4f}°")
        # print(
        #    f"                | hsv_cylinder_hue_angle={hsv_cylinder_hue_angle:8.4f}°")


# 角度を比較してみましょう
for (_, test_case) in enumerate(TEST_CASES):
    hsv_vs_hul_hue_angle_test(test_case[1], test_case[0])
