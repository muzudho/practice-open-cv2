"""色モデル"""

import math


def to_color_rate(vertical_parcent, theta):
    """
    vertical_parcent : [float, float, float]
        0.0～1.0 の値が３つ。１段目、２段目、３段目の順
    theta : float
        弧度法。0°を １２時の方向（赤）とし、
        時計回りに黄色、緑、青緑……、と進んでいきます
    """

    # 半径 1.0、 中心座標 (0,0) は省略
    # 欲しいのは 中心からの相対 y 座標 1.0 ～ -1.0 だけ
    n3bars_color_rate = (
        # 円周上の赤い点の位置 0.0～1.0
        -math.cos(math.radians(theta)),  # yは上下反転
        # 円周上の緑の点の位置
        -math.cos(math.radians(theta-120)),
        # 円周上の青の点の位置
        -math.cos(math.radians(theta+120)))

    diff_rate = __diff_for_fit(n3bars_color_rate, vertical_parcent[1])

    # 0.0 ～ 1.0 の比で返します
    return (
        n3bars_color_rate[0] + diff_rate[0] + vertical_parcent[2],
        n3bars_color_rate[1] + diff_rate[1] + vertical_parcent[2],
        n3bars_color_rate[2] + diff_rate[2] + vertical_parcent[2])


def __diff_for_fit(color_rate, diameter_rate):
    """フィットするための差分
    color_rate : (float, float, float)
        ２段目の箱の中に占める３本のバーの縦幅の割合 0.0～1.0
    diameter_rate : float
        箱全体に占める２段目の箱の縦幅の割合 0.0～1.0
    """

    if diameter_rate == 0.0:
        return (0.0, 0.0, 0.0)

    # print(f"red={color_rate[0]} green={color_rate[1]} blue={color_rate[2]}")

    longest = max(color_rate[0], color_rate[1], color_rate[2])
    shortest = min(color_rate[0], color_rate[1], color_rate[2])
    inner = longest - shortest
    zoom = inner / diameter_rate

    def one_diff(rate):
        inner = rate - shortest
        if zoom == 0:
            return 0  # 0除算が起こるなら（仕方が無いので）差分は 0 にします
        fit = int(inner / zoom)
        return fit - rate

    return (
        one_diff(color_rate[0]),
        one_diff(color_rate[1]),
        one_diff(color_rate[2]))
