"""RGBバーが出てくる矩形
"""


class BarWindow():
    """RGBバーが出てくる矩形
    """

    def __init__(self):
        self.__left_top = (0, 0)
        self.__right_bottom = (0, 0)

    @property
    def left_top(self):
        """箱の左上点"""
        return self.__left_top

    @left_top.setter
    def left_top(self, val):
        self.__left_top = val

    @property
    def right_bottom(self):
        """箱の右下点"""
        return self.__right_bottom

    @right_bottom.setter
    def right_bottom(self, val):
        self.__right_bottom = val
