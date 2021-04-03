"""HULモデル
MIT LICENSE

HSVモデルの仲間で、
色相と色調を扱うライブラリの実装です。
"""

import math


def to_color_rate(vertical_parcent, theta):
    """
    vertical_parcent : [float, float, float]
        合計 1.0 となる 0.0～1.0 の値が３つ。
        箱の１段目、２段目、３段目の順
    theta : float
        弧度法。0°を １２時の方向（赤）とし、
        時計回りに黄色、緑、青緑……、と進んでいきます
    """

    # 円周上の３点のx位置
    r_x = math.cos(math.radians(theta))
    g_x = math.cos(math.radians(theta-120))
    b_x = math.cos(math.radians(theta+120))

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

    # 'vertical_parcent[1]' - 箱全体に占める２段目の箱の縦幅の割合 0.0～1.0
    # 'vertical_parcent[2]' - 箱全体に占める３段目の箱の縦幅の割合 0.0～1.0
    # 0.0 ～ 1.0 の比で返します
    return (
        rrrx * vertical_parcent[1] + vertical_parcent[2],
        gggx * vertical_parcent[1] + vertical_parcent[2],
        bbbx * vertical_parcent[1] + vertical_parcent[2])


def __one_fit(rate, left_end, diff):
    """フィットさせます"""
    if diff == 0:
        return 0  # 0除算が起こるなら（仕方が無いので）差分は 0 にします
    return (rate-left_end) / diff
