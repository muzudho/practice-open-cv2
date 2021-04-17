"""エージェントの移動。
すべてのマスは 移動可能と考えた上で、制限をしていきます。
テキストは 左から右にしか進入させません。
"""


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


def move_up(board, agent):
    """↑上に移動"""
    cur_col = agent.location[0]
    cur_row = agent.location[1]

    # 現在マス
    if board.rows[cur_row][cur_col] in ('→', '↓', '←',
                                        '┌', '┐', '┘│', '│└',
                                        '┐┌', '─', '─┌', '┐─') or is_letter(board, agent.location):
        # 上を移動禁止とする現在マス
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

    if next_row >= 0 and next_col < len(board.checked_rows[next_row]) and \
            not board.checked_rows[next_row][next_col]:
        # 移動可能範囲内で、未チェックなら移動
        board.checked_rows[cur_row][cur_col] = True  # 移動前の位置をチェック
        agent.location[1] -= 1
        return True

    return False


def undo_move_up(agent):
    """↑上に移動しなかったことにする"""
    agent.location[1] += 1


def move_to_right(board, agent):
    """→右に移動"""
    cur_col = agent.location[0]
    cur_row = agent.location[1]

    if board.rows[cur_row][cur_col] in ('↑', '↓', '←', '┐', '┘',
                                        '│', '┘│', '┐│', '┘┐', '┐┘'):
        # 右を移動禁止とする現在マス
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

    if next_col < board.width and next_col < len(board.checked_rows[next_row]) and \
            not board.checked_rows[next_row][next_col]:
        # 移動可能範囲内で、未チェックなら移動可
        board.checked_rows[cur_row][cur_col] = True  # 移動前の位置をチェック
        agent.location[0] += 1
        return True

    return False


def undo_move_to_right(agent):
    """→右に移動しなかったことにする"""
    agent.location[0] -= 1


def move_down(board, agent):
    """↓下に移動"""
    cur_col = agent.location[0]
    cur_row = agent.location[1]

    if board.rows[cur_row][cur_col] in ('↑', '→', '←',
                                        '┘', '└', '─', '┘─', '─└', '┘└') \
            or is_letter(board, agent.location):
        # 下を移動禁止とする現在マス
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

    # 移動可能範囲内で、未チェックなら移動可
    if next_row < board.height and next_col < len(board.checked_rows[next_row]) and \
            not board.checked_rows[next_row][next_col]:
        board.checked_rows[cur_row][cur_col] = True  # 移動前の位置をチェック
        agent.location[1] += 1
        return True

    return False


def undo_move_down(agent):
    """↓下に移動しなかったことにする"""
    agent.location[1] -= 1


def move_to_left(board, agent):
    """←左に移動"""
    cur_col = agent.location[0]
    cur_row = agent.location[1]

    is_char = not is_rail(board, agent.location) and \
        len(board.rows[cur_row][cur_col]
            ) == 1 or board.rows[cur_row][cur_col] == '..'

    if board.rows[cur_row][cur_col] in ('↑', '→', '↓',
                                        '┌', '└', '│', '│┌', '│└', '└┌', '┌└') or is_char:
        # 左を移動禁止とする現在マス
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

    # 移動可能範囲内で、未チェックなら移動可
    if next_col > 0 and next_col < len(board.checked_rows[next_row]) and \
            not board.checked_rows[next_row][next_col]:
        board.checked_rows[cur_row][cur_col] = True  # 移動前の位置をチェック
        agent.location[0] -= 1
        return True

    return False


def undo_move_to_left(agent):
    """←左に移動しなかったことにする"""
    agent.location[0] += 1
