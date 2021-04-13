"""HULビューの入出力テスト
"""

import math
from conf import ACCURACY


def upper_test(seq, hul_phase, expected_upper, actual_upper, input_angle, color):
    """上限値(U)テスト
    """
    diff = actual_upper - expected_upper
    if not math.isclose(actual_upper, expected_upper, abs_tol=ACCURACY):
        print(
            f"ERROR           | seq={seq:5} phase={hul_phase} \
expected_upper={expected_upper:3} \
actual_upper={actual_upper:3} diff={diff} input_angle={input_angle} \
r={color[0]:9.4f} g={color[1]:9.4f} b={color[2]:9.4f}")
#    else:
#        print(
#            f"OK              | seq={seq:5} phase={hul_phase} \
#expected_upper={expected_upper:3} \
# actual_upper={actual_upper:3} diff={diff} input_angle={input_angle} \
# r={color[0]:9.4f} g={color[1]:9.4f} b={color[2]:9.4f}")


def lower_test(seq, hul_phase, expected_lower, actual_lower, input_angle, color):
    """下限値(U)テスト
    """
    diff = actual_lower - expected_lower
    if not math.isclose(actual_lower, expected_lower, abs_tol=ACCURACY):
        print(
            f"ERROR           | seq={seq:5} phase={hul_phase} \
expected_lower={expected_lower:3} \
actual_lower={actual_lower:3} diff={diff} input_angle={input_angle} \
r={color[0]:9.4f} g={color[1]:9.4f} b={color[2]:9.4f}")
#    else:
#        print(
#            f"OK              | seq={seq:5} phase={hul_phase} \
#expected_lower={expected_lower:3} \
# actual_lower={actual_lower:3} diff={diff} input_angle={input_angle} \
# r={color[0]:9.4f} g={color[1]:9.4f} b={color[2]:9.4f}")


def hue_angle_test(seq, hul_phase, input_angle, actual_angle, color, tolerance):
    """色相(H)テスト
    """
    diff_angle = actual_angle - input_angle
    # float型には無限小の丸め誤差が出るものなので、 誤差 0 はあり得ない。等号での比較はしてはいけないぜ（＾～＾）
    if tolerance < diff_angle:
        upper = max(color[0], color[1], color[2])
        lower = min(color[0], color[1], color[2])
        bar_length = color[0] + color[1] + color[2] - upper - lower
        width = bar_length - lower
        diameter = upper - lower
        radius = diameter / 2
        print(
            f"ERROR           | seq={seq:5} phase={hul_phase:3} \
exp={input_angle:10.6f}° act={actual_angle:10.6f}° \
diff={diff_angle:10.6f}° r={color[0]:9.6f} g={color[1]:9.6f} b={color[2]:9.6f} \
up={upper:9.6f} low={lower:9.6f} \
width={width:9.6f} radius={radius:9.6f}")
#    else:
#        upper = max(color[0], color[1], color[2])
#        lower = min(color[0], color[1], color[2])
#        bar_length = color[0] + color[1] + color[2] - upper - lower
#        width = bar_length - lower
#        diameter = upper - lower
#        radius = diameter / 2
#        print(
#            f"OK              | seq={seq:5} phase={hul_phase:3} \
# exp={input_angle:10.6f}° act={actual_angle:10.6f}° \
# diff={diff_angle:10.6f}° r={color[0]:9.6f} g={color[1]:9.6f} b={color[2]:9.6f} \
# up={upper:9.6f} low={lower:9.6f} \
# width={width:9.6f} radius={radius:9.6f}")

    return diff_angle
