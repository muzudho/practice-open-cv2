"""cv2のための変換関数"""


def point_for_cv2(point):
    """floatをintへ変換"""
    return (int(point[0]), int(point[1]))


def color_for_cv2(color):
    """0.0～1.0 を、cv2の色値域 0～255 に合わせます"""
    return (
        int(255*color[0]),
        int(255*color[1]),
        int(255*color[2]))
