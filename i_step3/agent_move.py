"""エージェントの移動。
すべてのマスは 移動可能と考えた上で、制限をしていきます。
テキストは 左から右にしか進入させません。
"""


def can_proceed(board, location):
    """進むことができます"""
    return location[1] < board.height and location[0] < len(board.checked_rows[location[1]]) and \
        not board.checked_rows[location[1]][location[0]]


def is_rail(board, location):
    """罫線、矢印なら真"""
    return board.rows[location[1]][location[0]] in (
        '↑', '→', '↓', '←',  # 矢印
        '┌', '┐', '┘', '└', '┌r', '┐r', '┘r', '└r',  # コーナー
        '│', '─',  # 一直線
        '┘─', '─└', '┘└',  # 上分岐
        '│┌', '│└', '└┌', '┌└',  # 右分岐
        '─┌', '┐─', '┐┌',  # 下分岐
        '┐│', '┘│', '┘┐', '┐┘')  # 左分岐


def is_letter(board, location):
    """テキストなら真。ただし一文字の矢印などは含めない"""
    return not is_rail(board, location) and \
        (len(board.rows[location[1]][location[0]]
             ) == 1 or board.rows[location[1]][location[0]] == '..')


def can_move_up(board, agent, prev_location):
    """↑上に移動できるか"""
    # １つ前のマス
    pre_col = prev_location[0]

    # 現在マス
    cur_col = agent.location[0]
    cur_row = agent.location[1]
    cur_sq = board.rows[cur_row][cur_col]

    # 上への移動を禁止とする現在マス
    forbidden = cur_sq in ('',  # 何もないところ
                           '→', '↓', '←',  # 矢印
                           '┌', '┐', '┌r', '┐r',  # コーナー
                           '─',  # 一直線
                           '┐┌', '─┌', '┐─')  # 下分岐
    if forbidden or is_letter(board, agent.location):
        return False

    # 右から上へは行けない
    forbidden_from_right = cur_sq in ('│┌', '┘─') and cur_col == pre_col-1
    # 右から上へは行けない
    forbidden_from_left = cur_sq in ('┐│', '─└') and cur_col == pre_col+1
    # １つ前の位置によっては、上への移動を禁止とする現在マス
    if forbidden_from_right or forbidden_from_left:
        return False

    next_col = cur_col
    next_row = cur_row - 1

    # 下からの進入を禁止する移動先マス
    forbidden = board.rows[next_row][next_col] in ('',  # 何もないところ
                                                   '→', '↓', '←',  # 矢印
                                                   '┘', '└', '┘r', '└r',  # コーナー
                                                   '─',  # 一直線
                                                   '┘─', '─└', '┘└')  # 上分岐
    if forbidden or is_letter(board, agent.location):
        return False

    # 移動可能範囲外、またはチェック済み
    if not can_proceed(board, (next_col, next_row)):
        return False

    return True


def move_up(agent):
    """↑上に移動"""
    agent.location[1] -= 1


def undo_move_up(agent):
    """↑上に移動しなかったことにする"""
    agent.location[1] += 1


def can_move_to_right(board, agent, prev_location):
    """→右に移動できるか"""
    # １つ前のマス
    _pre_col = prev_location[0]
    pre_row = prev_location[1]

    # 現在マス
    cur_col = agent.location[0]
    cur_row = agent.location[1]
    cur_sq = board.rows[cur_row][cur_col]

    # 右への移動を禁止とする現在マス
    if cur_sq in ('',  # 何もないところ
                  '↑', '↓', '←',  # 矢印
                  '┐', '┘', '┐r', '┘r',  # コーナー
                  '│',  # 一直線
                  '┘│', '┐│', '┘┐', '┐┘'):  # 左分岐
        return False

    # 上から右へは行けない
    forbidden_from_up = cur_sq in ('│┌', '┘─') and cur_row == pre_row-1
    # 下から右へは行けない
    forbidden_from_down = cur_sq in ('│└', '┐─') and cur_row == pre_row+1
    if forbidden_from_up or forbidden_from_down:
        return False

    next_col = cur_col + 1
    next_row = cur_row

    # 左からの進入を禁止する移動先マス
    forbidden = board.rows[next_row][next_col] in ('',  # 何もないところ
                                                   '↑', '↓', '←',  # 矢印
                                                   '┌', '└', '┌r', '└r',  # コーナー
                                                   '│',  # 一直線
                                                   '│┌', '│└', '└┌', '┌└')  # 右分岐
    if forbidden:
        return False

    # 移動可能範囲外、またはチェック済み
    if not can_proceed(board, (next_col, next_row)):
        return False

    return True


def move_to_right(agent):
    """→右に移動"""
    agent.location[0] += 1


def undo_move_to_right(agent):
    """→右に移動しなかったことにする"""
    agent.location[0] -= 1


def can_move_down(board, agent, prev_location):
    """↓下に移動できるか"""
    # １つ前のマス
    pre_col = prev_location[0]
    _pre_row = prev_location[1]

    # 現在マス
    cur_col = agent.location[0]
    cur_row = agent.location[1]
    cur_sq = board.rows[cur_row][cur_col]

    # 下への移動を禁止とする現在マス
    forbidden = cur_sq in ('',  # 何もないところ
                           '↑', '→', '←',  # 矢印
                           '┘', '└', '┘r', '└r',  # コーナー
                           '─',  # 一直線
                           '┘─', '─└', '┘└')  # 上分岐
    if forbidden or is_letter(board, agent.location):
        return False

    # 右から下へは行けない
    forbidden_from_right = cur_sq in ('│└', '┐─') and cur_col == pre_col-1
    # 左から下へは行けない
    forbidden_from_left = cur_sq in ('┘│', '─┌') and cur_col == pre_col+1
    if forbidden_from_right or forbidden_from_left:
        return False

    next_col = cur_col
    next_row = cur_row + 1

    # 上からの進入を禁止する移動先マス
    forbidden = board.rows[next_row][next_col] in ('',  # 何もないところ
                                                   '↑', '→', '←',  # 矢印
                                                   '┌', '┐', '┌r', '┐r',  # コーナー
                                                   '─',  # 一直線
                                                   '─┌', '┐─', '┐┌')  # 下分岐
    if forbidden or is_letter(board, agent.location):
        return False

    # 移動可能範囲外、またはチェック済み
    if not can_proceed(board, (next_col, next_row)):
        return False

    return True


def move_down(agent):
    """↓下に移動"""
    agent.location[1] += 1


def undo_move_down(agent):
    """↓下に移動しなかったことにする"""
    agent.location[1] -= 1


def can_move_to_left(board, agent, prev_location):
    """←左に移動できるか"""
    # １つ前のマス
    _pre_col = prev_location[0]
    pre_row = prev_location[1]

    # 現在マス
    cur_col = agent.location[0]
    cur_row = agent.location[1]
    cur_sq = board.rows[cur_row][cur_col]

    # 左への移動を禁止とする現在マス
    forbidden = cur_sq in ('',  # 何もないところ
                           '↑', '→', '↓',  # 矢印
                           '┌', '└', '┌r', '└r',  # コーナー
                           '│',  # 一直線
                           '│┌', '│└', '└┌', '┌└')  # 左分岐

    if forbidden or is_letter(board, agent.location):
        # 左を移動禁止とする現在マス
        return False

    # 上から左へはいけない
    forbidden_from_top = cur_sq in ('┐│', '─└') and cur_row == pre_row+1
    # 下から左へはいけない
    forbidden_from_bottom = cur_sq in ('┘│', '─┌') and cur_row == pre_row-1
    if forbidden_from_top or forbidden_from_bottom:
        return False

    next_col = cur_col - 1
    next_row = cur_row

    # 右からの進入を禁止する移動先マス
    forbidden = board.rows[next_row][next_col] in ('',  # 何もないところ
                                                   '↑', '→', '↓',  # 矢印
                                                   '┐', '┘', '┐r', '┘r',  # コーナー
                                                   '│',  # 一直線
                                                   '┐│', '┘│', '┘┐', '┐┘')  # 左分岐
    if forbidden or is_letter(board, agent.location):
        return False

    # 移動可能範囲外、またはチェック済み
    if not can_proceed(board, (next_col, next_row)):
        return False

    return True


def move_to_left(agent):
    """←左に移動"""
    agent.location[0] -= 1


def undo_move_to_left(agent):
    """←左に移動しなかったことにする"""
    agent.location[0] += 1
