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
    # n3y_on_circumference : (float, float, float)
    #     ２段目の箱の中に占める３本のバーの縦幅の割合 0.0～1.0
    n3y_on_circumference = (
        # 円周上の赤い点の位置 0.0～1.0
        -math.cos(math.radians(theta)),  # yは上下反転
        # 円周上の緑の点の位置
        -math.cos(math.radians(theta-120)),
        # 円周上の青の点の位置
        -math.cos(math.radians(theta+120)))
    print(
        f"n3y_on_circumference=({n3y_on_circumference[0]}, {n3y_on_circumference[1]}, \
{n3y_on_circumference[2]})")

    # -1.0 ～ 1.0 を 0 ～ 2.0 に変換してから長短を調べます
    n3y_in_diameter = (
        n3y_on_circumference[0] + 1.0,
        n3y_on_circumference[1] + 1.0,
        n3y_on_circumference[2] + 1.0)
    if not 0.0 <= n3y_in_diameter[0] <= 2.0:
        raise Exception(f"red={n3y_in_diameter[0]}")
    if not 0.0 <= n3y_in_diameter[1] <= 2.0:
        raise Exception(f"green={n3y_in_diameter[0]}")
    if not 0.0 <= n3y_in_diameter[2] <= 2.0:
        raise Exception(f"blue={n3y_in_diameter[0]}")
    longest = max(n3y_in_diameter[0], n3y_in_diameter[1], n3y_in_diameter[2])
    if not 0.0 <= longest <= 2.0:
        raise Exception(f"longest={longest}")
    shortest = min(n3y_in_diameter[0], n3y_in_diameter[1], n3y_in_diameter[2])
    if not 0.0 <= shortest <= 2.0:
        raise Exception(f"shortest={shortest}")
    length = longest - shortest
    if not 0.0 <= length <= 2.0:
        raise Exception(f"length={length}")
    zoom = length / 2.0
    if not 0.0 <= zoom <= 1.0:
        raise Exception(f"zoom={zoom}")
    print(f"longest={longest} shortest={shortest} length={length} zoom={zoom}")

    fit_to_diameter = (
        __one_fit(n3y_in_diameter[0], zoom),
        __one_fit(n3y_in_diameter[1], zoom),
        __one_fit(n3y_in_diameter[2], zoom))

    print(
        f"fit_to_diameter=({fit_to_diameter[0]}, {fit_to_diameter[1]}, {fit_to_diameter[2]})")
    print(f"vertical_parcent[2]={vertical_parcent[2]}")

    # 'vertical_parcent[1]' - 箱全体に占める２段目の箱の縦幅の割合 0.0～1.0
    # 'vertical_parcent[2]' - 箱全体に占める３段目の箱の縦幅の割合 0.0～1.0
    # 0.0 ～ 1.0 の比で返します
    return (
        fit_to_diameter[0] * vertical_parcent[1] + vertical_parcent[2],
        fit_to_diameter[1] * vertical_parcent[1] + vertical_parcent[2],
        fit_to_diameter[2] * vertical_parcent[1] + vertical_parcent[2])


def __one_fit(rate, zoom):
    """フィットさせます"""
    if zoom == 0:
        return 0  # 0除算が起こるなら（仕方が無いので）差分は 0 にします
    return rate / zoom
