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

VIVID_RED = (1.0, 0.0, 0.0)
# 赤を 60° とするよう HULモデルを調整します
HUL_TO_HSV_ANGLE = 60

# 角度を比較してみましょう
hul_hue_angle, _ = to_hul_hue_angle(VIVID_RED)
hul_hue_angle += HUL_TO_HSV_ANGLE
hsv_cone_hue_angle = to_hsv_cone_hue_angle(VIVID_RED)
hsv_cylinder_hue_angle = to_hsv_cylinder_hue_angle(VIVID_RED)
print(f"VIVID_RED             ={VIVID_RED}°")
print(f"hul_hue_angle         ={hul_hue_angle:8.4f}°")
print(f"hsv_cone_hue_angle    ={hsv_cone_hue_angle:8.4f}°")
print(f"hsv_cylinder_hue_angle={hsv_cylinder_hue_angle:8.4f}°")
