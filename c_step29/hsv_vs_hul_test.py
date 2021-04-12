"""HSVモデルとHULビューの比較を行います
"""

from hsv_model_hul_view import to_hue_angle as to_hul_hue_angle
from hsv_model_cone import to_hue_angle as to_hsv_cone_hue_angle
from hsv_model_cylinder import to_hue_angle as to_hsv_cylinder_hue_angle

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
    ((1.0, 0.0, 0.0), 'Vivid red'),
    ((0.0, 1.0, 0.0), 'Vivid green'),
    ((0.0, 0.0, 1.0), 'Vivid blue'),
]

# 角度を比較してみましょう
for (_, test_case) in enumerate(TEST_CASES):
    hul_hue_angle, _ = to_hul_hue_angle(test_case[0])
    hsv_cone_hue_angle = to_hsv_cone_hue_angle(test_case[0])
    hsv_cylinder_hue_angle = to_hsv_cylinder_hue_angle(test_case[0])
    print(f"{test_case[1]:22}={test_case[1]}")
    print(f"hul_hue_angle         ={hul_hue_angle:8.4f}°")
    print(f"hsv_cone_hue_angle    ={hsv_cone_hue_angle:8.4f}°")
    print(f"hsv_cylinder_hue_angle={hsv_cylinder_hue_angle:8.4f}°")
