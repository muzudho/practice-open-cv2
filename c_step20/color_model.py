"""色モデル
MIT LICENSE

ライブラリによって、
0° がどちら向きか、
回転方向は 時計回りか、逆時計回りか、
y は どちらが上か
異なるので、実装者は 調整してください。

12時の方向を 0°、 時計回りに 赤、黄色、緑 と
進むものとします。
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

    # 半径 1.0、 中心座標 (0,0) は省略
    # 欲しいのは 中心からの相対 y 座標 1.0 ～ -1.0 だけ
    n3y_on_circumference = (
        # 円周上の赤い点の位置 0.0～1.0
        math.cos(math.radians(theta)),  # yは上下反転
        # 円周上の緑の点の位置
        math.cos(math.radians(theta-120)),
        # 円周上の青の点の位置
        math.cos(math.radians(theta+120)))

    # -1.0 ～ 1.0 に +1.0 を足して 0.0 ～ 2.0 に変形し、
    # 扱いやすいように 2 で割って 0.0 ～ 1.1 にします
    n3y_in_diameter = (
        (n3y_on_circumference[0] + 1.0) / 2,
        (n3y_on_circumference[1] + 1.0) / 2,
        (n3y_on_circumference[2] + 1.0) / 2)

    longest = max(n3y_in_diameter[0], n3y_in_diameter[1], n3y_in_diameter[2])
    shortest = min(n3y_in_diameter[0], n3y_in_diameter[1], n3y_in_diameter[2])

    # shortest ～ x ～ longest という数は使いにくいので、 0.0 ～ 1.0 にフィッティングさせます。
    # これは結局、 x を微調整するための働きです

    gap = longest - shortest

    fit_to_diameter = (
        __one_fit(n3y_in_diameter[0], shortest, gap),
        __one_fit(n3y_in_diameter[1], shortest, gap),
        __one_fit(n3y_in_diameter[2], shortest, gap))

    # 'vertical_parcent[1]' - 箱全体に占める２段目の箱の縦幅の割合 0.0～1.0
    # 'vertical_parcent[2]' - 箱全体に占める３段目の箱の縦幅の割合 0.0～1.0
    # 0.0 ～ 1.0 の比で返します
    return (
        fit_to_diameter[0] * vertical_parcent[1] + vertical_parcent[2],
        fit_to_diameter[1] * vertical_parcent[1] + vertical_parcent[2],
        fit_to_diameter[2] * vertical_parcent[1] + vertical_parcent[2])


def __one_fit(rate, shortest, gap):
    """フィットさせます"""
    if gap == 0:
        return 0  # 0除算が起こるなら（仕方が無いので）差分は 0 にします
    return (rate-shortest) / gap
