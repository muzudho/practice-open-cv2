"""色モデル"""

import math


class ColorModel():
    """色モデル"""

    def __init__(self):
        """初期化"""

    def color(self, vertical_parcent, theta):
        """
        vertical_parcent : [float, float, float]
            0.0～1.0 の値が３つ。１段目、２段目、３段目の順
        theta : float
            弧度法。0°を １２時の方向（赤）とし、
            時計回りに黄色、緑、青緑……、と進んでいきます
        """
        rng = 1.0  # range
        color_rate = (
            # 円周上の赤い点の位置 0.0～1.0
            (int(rng * math.sin(math.radians(theta))),
             int(-rng * math.cos(math.radians(theta)))),  # yは上下反転
            # 円周上の緑の点の位置
            (int(rng * math.sin(math.radians(theta-120))),
             int(-rng * math.cos(math.radians(theta-120)))),
            # 円周上の青の点の位置
            (int(rng * math.sin(math.radians(theta+120))),
             int(-rng * math.cos(math.radians(theta+120)))))

        def diff_for_fit(color_rate, diameter_rate):
            """フィットするための差分
            color_rate : (float, float, float)
                ２段目の箱の中に占める３本のバーの縦幅の割合 0.0～1.0
            diameter_rate : float
                箱全体に占める２段目の箱の縦幅の割合 0.0～1.0
            """

            if diameter_rate == 0.0:
                return (0.0, 0.0, 0.0)

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

        diameter_rate = vertical_parcent[1]
        diff_rate = diff_for_fit(color_rate, diameter_rate)
        color_rate = (
            color_rate[0] + diff_rate[0] + vertical_parcent[2],
            color_rate[1] + diff_rate[1] + vertical_parcent[2],
            color_rate[2] + diff_rate[2] + vertical_parcent[2])

        # 0～255 に変換
        return(
            255*color_rate[0],
            255*color_rate[1],
            255*color_rate[2])
