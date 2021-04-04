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
    (3, (UPPER, 81, LOWER)),
]


def calc(upper, lower, expected_h_deg, color):
    """テスト"""
    r_x = color[0] - lower
    g_x = color[1] - lower
    _diameter = upper - lower
    # rad = color[1]/color[0]
    rad = g_x/r_x
    # print(
    #    f"r_x={r_x} g_x={g_x} diameter={diameter} rad={rad}")
    actual_h_deg = math.degrees(math.asin(rad))
    if expected_h_deg != actual_h_deg:
        print(
            f"ERROR           | expected_h_deg={expected_h_deg}° actual_h={actual_h_deg:9.4f}°")


for test_case in TEST_CASES:
    calc(UPPER, LOWER, test_case[0], test_case[1])
