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
    print(
        f"n3bars_color_rate=({n3bars_color_rate[0]}, {n3bars_color_rate[1]}, \
{n3bars_color_rate[2]})")

    fit_color_rate = __fit_color_rate(n3bars_color_rate, vertical_parcent[1])
    print(
        f"fit_color_rate=({fit_color_rate[0]}, {fit_color_rate[1]}, {fit_color_rate[2]})")
    print(f"vertical_parcent[2]={vertical_parcent[2]}")

    # 0.0 ～ 1.0 の比で返します
    return (
        fit_color_rate[0] + vertical_parcent[2],
        fit_color_rate[1] + vertical_parcent[2],
        fit_color_rate[2] + vertical_parcent[2])


def __fit_color_rate(color_rate, diameter_rate):
    """フィット
    color_rate : (float, float, float)
        ２段目の箱の中に占める３本のバーの縦幅の割合 0.0～1.0
    diameter_rate : float
        箱全体に占める２段目の箱の縦幅の割合 0.0～1.0
    """

    if diameter_rate == 0.0:
        return (0.0, 0.0, 0.0)

    # print(f"red={color_rate[0]} green={color_rate[1]} blue={color_rate[2]}")

    # -1.0 ～ 1.0 を 0 ～ 2.0 に変換してから長短を調べます
    longest = max(color_rate[0]+1.0, color_rate[1]+1.0, color_rate[2]+1.0)
    shortest = min(color_rate[0]+1.0, color_rate[1]+1.0, color_rate[2]+1.0)
    inner = longest - shortest
    zoom = inner / diameter_rate
    print(f"longest={longest} shortest={shortest} inner={inner} zoom={zoom}")

    return (
        __one_diff(color_rate[0], zoom),
        __one_diff(color_rate[1], zoom),
        __one_diff(color_rate[2], zoom))


def __one_diff(rate, zoom):
    """フィットさせます"""
    if zoom == 0:
        return 0  # 0除算が起こるなら（仕方が無いので）差分は 0 にします
    return rate / zoom
