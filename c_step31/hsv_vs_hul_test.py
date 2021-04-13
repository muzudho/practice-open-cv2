"""HSVモデル(円錐モデル)とHULビューの比較を行います
"""

from hsv_model_hul_view import to_hue_angle as to_hul_hue_angle, hul_to_color
from hsv_model_cone import to_hue_angle as to_hsv_cone_hue_angle, to_color as hsv_to_color

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
# (色, 角度(弧度法,整数), タイトル)
TEST_CASES = [
    # ３色相
    ((1.0, 0.0, 0.0), 0, 'Vivid red'),
    ((0.0, 1.0, 0.0), 120, 'Vivid green'),
    ((0.0, 0.0, 1.0), 240, 'Vivid blue'),

    # ６色相
    ((1.0, 1.0, 0.0), 60, 'Vivid yellow'),
    ((0.0, 1.0, 1.0), 180, 'Vivid cyan'),
    ((1.0, 0.0, 1.0), 300, 'Vivid magenta'),

    # １２色相
    ((1.0, 0.5, 0.0), 30, 'Vivid orange'),
    ((0.5, 1.0, 0.0), 90, 'Vivid yellow green'),
    ((0.0, 1.0, 0.5), 150, 'Vivid blue green'),
    ((0.0, 0.5, 1.0), 210, 'Vivid dodgers blue'),
    ((0.5, 0.0, 1.0), 270, 'Vivid indigo'),
    ((1.0, 0.0, 0.5), 330, 'Vivid crimson'),

    # ２４色相
    ((1.00, 0.25, 0.00), 15, 'Vivid red+'),
    ((1.00, 0.75, 0.00), 45, 'Vivid orange+'),
    ((0.75, 1.00, 0.00), 75, 'Vivid yellow+'),
    ((0.25, 1.00, 0.00), 105, 'Vivid yellow green+'),
    ((0.00, 1.00, 0.25), 135, 'Vivid green+'),
    ((0.00, 1.00, 0.75), 165, 'Vivid blue green+'),
    ((0.00, 0.75, 1.00), 195, 'Vivid cyan+'),
    ((0.00, 0.25, 1.00), 225, 'Vivid dodgers blue+'),
    ((0.25, 0.00, 1.00), 255, 'Vivid blue+'),
    ((0.75, 0.00, 1.00), 285, 'Vivid indigo+'),
    ((1.00, 0.00, 0.75), 315, 'Vivid magenta+'),
    ((1.00, 0.00, 0.25), 345, 'Vivid crimson+'),
]


def hsv_vs_hul_hue_angle_test(title, color, tolerance):
    """HSVとHULの色相(H)が等しいかテスト。
    HUL は 整数の精度しかありませんので、 HSV の方を丸めます
    """
    hul_hue_angle, description = to_hul_hue_angle(color)
    hsv_cone_hue_angle = to_hsv_cone_hue_angle(color)
    round_hsv_cone_hue_angle = round(hsv_cone_hue_angle)
    # hsv_cylinder_hue_angle = to_hsv_cylinder_hue_angle(color)
    # 誤差が許容半径を超えたら表示します
    diff = abs(hul_hue_angle - round_hsv_cone_hue_angle)
    if tolerance < diff:
        # if not math.isclose(hul_hue_angle, hsv_cone_hue_angle, \
        # rel_tol=ACCURACY, abs_tol=ACCURACY):
        # or not math.isclose(hul_hue_angle, hsv_cylinder_hue_angle,
        #                 rel_tol = ACCURACY, abs_tol = ACCURACY):
        print(f"Angle test      | {title:22} color={color}")
        print(
            f"                | hul_hue_angle         ={hul_hue_angle:4}° {description[2]}")
        print(
            f"                | hsv_cone_hue_angle    ={round_hsv_cone_hue_angle:4}° \
{hsv_cone_hue_angle:8.4f}°")
        # print(
        #    f"                | hsv_cylinder_hue_angle={hsv_cylinder_hue_angle:8.4f}°")
    # else:
    #    print(f"Angle test      | {title:22} color={color}")
    #    print(
    #        f"                | hul_hue_angle         ={hul_hue_angle:4}° {description[2]}")
    #    print(
    #        f"                | hsv_cone_hue_angle    ={round_hsv_cone_hue_angle:4}° \
    # {hsv_cone_hue_angle:8.4f}°")


def hsv_vs_hul_vivid_color_test(title, hue_angle, tolerance):
    """HSVとHULの色（Vivid tone）が等しいかテスト"""
    hul_color = hul_to_color(hue_angle, 1.0, 0.0)  # Vivid
    hsv_color = hsv_to_color(hue_angle, 1.0, 1.0)  # Vivid
    # 誤差が許容半径を超えたら表示します
    diff_r = abs(hul_color[0] - hsv_color[0])
    diff_g = abs(hul_color[1] - hsv_color[1])
    diff_b = abs(hul_color[2] - hsv_color[2])
    if tolerance < diff_r or tolerance < diff_g or tolerance < diff_b:
        print(f"Color test      | {title:22} hue_angle={hue_angle:4}°")
        print(
            f"                | hul_color =({hul_color[0]:13.10f}, {hul_color[1]:13.10f}, \
{hul_color[2]:13.10f})")
        print(
            f"                | hsv_color =({hsv_color[0]:13.10f}, {hsv_color[1]:13.10f}, \
{hsv_color[2]:13.10f})")


# 角度を比較してみましょう
for (_, test_case) in enumerate(TEST_CASES):
    hsv_vs_hul_hue_angle_test(test_case[2], test_case[0], 1.0000001)

# 色を比較してみましょう
for (_, test_case) in enumerate(TEST_CASES):
    hsv_vs_hul_vivid_color_test(test_case[2], test_case[1], 0.02)
