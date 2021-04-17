"""キャンバスを盤として捉えます"""


class Board():
    """キャンバスを盤として捉えます"""

    def __init__(self):
        self.__rows = []
        self.__checked_table = []
        self.__start_location = [0, 0]
        self.__width = 0
        self.__height = 0

    @property
    def rows(self):
        """テーブル"""
        return self.__rows

    @property
    def checked_table(self):
        """踏破済みチェックテーブル"""
        return self.__checked_table

    @property
    def start_location(self):
        """スタート地点"""
        return self.__start_location

    @start_location.setter
    def start_location(self, val):
        self.__start_location = val

    @property
    def width(self):
        """列数"""
        return self.__width

    @width.setter
    def width(self, val):
        self.__width = val

    @property
    def height(self):
        """行数"""
        return self.__height

    @height.setter
    def height(self, val):
        self.__height = val


def read_screen_csv(file_path):
    """入力ファイルを読み込みます"""

    # カンマ区切り テキスト。 UTF-8 with BOM の先頭の BOMコードを取り除くため 'utf_8_sig'
    with open(file_path, encoding='utf_8_sig') as file:
        text = file.read()

    board = Board()

    # 最大列、最大行を求めます
    lines = text.split('\n')
    board.height = len(lines)
    board.width = 0
    for (row, line) in enumerate(lines):
        cells = line.split(',')
        cells_num = len(cells)
        if board.width < cells_num:
            board.width = cells_num

        columns = []
        checked_columns = []
        for (column, cell) in enumerate(cells):
            cell = cell.strip()
            columns.append(cell)
            checked_columns.append(False)

            if cell == 'Start':
                board.start_location = [column, row]
        board.rows.append(columns)
        board.checked_table.append(checked_columns)

    return board
