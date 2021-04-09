"""cv2のための変換関数"""


def point_for_cv2(point):
    """floatをintへ変換"""
    return (int(point[0]), int(point[1]))
