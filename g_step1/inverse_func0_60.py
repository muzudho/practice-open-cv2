"""角度 0°～60°
赤がU
緑が変動
青がL
"""

import math

UPPER = 153
LOWER = 76
TEST_CASES = [
    (0, (UPPER, 76, LOWER)),
    (1, (UPPER, 77, LOWER)),
    (2, (UPPER, 79, LOWER)),
    (3, (UPPER, 80, LOWER)),
    (4, (UPPER, 81, LOWER)),
    (5, (UPPER, 83, LOWER)),
    (6, (UPPER, 84, LOWER)),
    (7, (UPPER, 86, LOWER)),
    (8, (UPPER, 87, LOWER)),
    (9, (UPPER, 89, LOWER)),
    (10, (UPPER, 90, LOWER)),
    (11, (UPPER, 91, LOWER)),
    (12, (UPPER, 92, LOWER)),
    (13, (UPPER, 93, LOWER)),
    (14, (UPPER, 95, LOWER)),
    (15, (UPPER, 96, LOWER)),
    (16, (UPPER, 97, LOWER)),
    (17, (UPPER, 99, LOWER)),
    (18, (UPPER, 100, LOWER)),
    (19, (UPPER, 101, LOWER)),
    (20, (UPPER, 102, LOWER)),
    (21, (UPPER, 103, LOWER)),
    (22, (UPPER, 104, LOWER)),
    (23, (UPPER, 106, LOWER)),
    (24, (UPPER, 107, LOWER)),
    (25, (UPPER, 108, LOWER)),
    (26, (UPPER, 109, LOWER)),
    (27, (UPPER, 111, LOWER)),
    (28, (UPPER, 112, LOWER)),
    (29, (UPPER, 112, LOWER)),
    (30, (UPPER, 113, LOWER)),
    (31, (UPPER, 115, LOWER)),
    (32, (UPPER, 116, LOWER)),
    (33, (UPPER, 117, LOWER)),
    (34, (UPPER, 119, LOWER)),
    (35, (UPPER, 120, LOWER)),
    (36, (UPPER, 121, LOWER)),
    (37, (UPPER, 122, LOWER)),
    (38, (UPPER, 123, LOWER)),
    (39, (UPPER, 124, LOWER)),
    (40, (UPPER, 125, LOWER)),
]


def calc(expected_h_deg, color):
    """テスト"""
    #upper = max(color[0], color[1], color[2])
    lower = min(color[0], color[1], color[2])
    #diameter = upper - lower
    r_x = color[0] - lower
    g_x = color[1] - lower
    #r_x = (color[0] - lower)/diameter
    #g_x = (color[1] - lower)/diameter
    # rad = color[1]/color[0]
    rad = g_x/r_x
    # print(
    #    f"r_x={r_x} g_x={g_x} diameter={diameter} rad={rad}")
    actual_h_deg = math.degrees(math.asin(rad))

    # 誤差 +-1 まで許容
    if actual_h_deg < expected_h_deg - 1.0 or expected_h_deg + 1.0 < actual_h_deg:
        diff = actual_h_deg - expected_h_deg
        print(
            f"ERROR           | expected_h_deg={expected_h_deg}° actual_h={actual_h_deg:9.4f}° diff={diff:9.4f} color({color[0]}, {color[1]}, {color[2]})")
        return False

    return True


total_num = 0
success_num = 0
for test_case in TEST_CASES:
    if calc(test_case[0], test_case[1]):
        success_num += 1
    total_num += 1

rate = (success_num/total_num)*100
print(f"成功率{rate:7.2f}％ {success_num}/{total_num}")
