"""cv2のための変換関数"""

from gamma_correction import de_gamma


def point_for_cv2(point):
    """floatをintへ変換"""
    return (int(point[0]), int(point[1]))


def color_for_cv2(color):
    """0.0～1.0 を、cv2の色値域 0～255 に合わせます"""

    # ガンマ補正を解除します
    # color = de_gamma(color)

    # 0.0～1.0 スケールを 0～255 スケールに変更します
    color = (
        int(255*color[0]),
        int(255*color[1]),
        int(255*color[2]))

    return color
