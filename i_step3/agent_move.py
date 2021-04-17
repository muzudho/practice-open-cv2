"""エージェントの移動
"""


def move_up(board, agent):
    """↑上に移動"""
    cur_col = agent.location[0]
    cur_row = agent.location[1]

    # 現在マス
    if board.rows[cur_row][cur_col] in ('→', '↓', '←', '┌', '┐', '┘│', '│└', '┐┌', '─┌', '┐─'):
        # 上を移動禁止とする現在マス
        return False

    next_col = cur_col
    next_row = cur_row - 1

    if next_row >= 0 and next_col < len(board.checked_rows[next_row]) and \
            not board.checked_rows[next_row][next_col]:
        # 次マス
        if board.rows[next_row][next_col] in ('┌', '┐', '┌r', '┐r',
                                              '│', '│┌', '┐│', '┘│', '│└', '┐┌', '┘┐', '┐┘', '└┌', '┌└'):
            # 道
            board.checked_rows[cur_row][cur_col] = True  # 移動前の位置をチェック
            agent.location[1] -= 1
            return True

        if len(board.rows[next_row][next_col]) == 1 or board.rows[next_row][next_col] == '..':
            # 文字
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

    if board.rows[cur_row][cur_col] in ('↑', '↓', '←', '┐', '┘', '┘│', '┐│', '┘┐', '┐┘'):
        # 右を移動禁止とする現在マス
        return False

    next_col = cur_col + 1
    next_row = cur_row

    if next_col < board.width and next_col < len(board.checked_rows[next_row]) and not board.checked_rows[next_row][next_col]:
        # 道
        if board.rows[next_row][next_col] in ('┐', '┘', '┐r', '┘r',
                                              '─', '─┌', '┐─', '┘─', '─└', '┘┐', '┐┘'):
            board.checked_rows[cur_row][cur_col] = True  # 移動前の位置をチェック
            agent.location[0] += 1
            return True

        if len(board.rows[next_row][next_col]) == 1 or board.rows[next_row][next_col] == '..':
            # 文字
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

    if board.rows[cur_row][cur_col] in ('↑', '→', '←', '┘', '└', '─', '┘─', '─└', '┘└'):
        # 下を移動禁止とする現在マス
        return False

    next_col = cur_col
    next_row = cur_row + 1

    if next_row < board.height and next_col < len(board.checked_rows[next_row]) and \
            not board.checked_rows[next_row][next_col]:
        # 道
        if board.rows[next_row][next_col] in ('┘', '└', '┘r', '└r',
                                              '│', '│┌', '┐│', '┘│', '│└', '┘└', '┘┐', '┐┘', '└┌', '┌└'):
            board.checked_rows[next_row][next_col] = True  # 移動前の位置をチェック
            agent.location[1] += 1
            return True

        if len(board.rows[next_row][next_col]) == 1 or board.rows[next_row][next_col] == '..':
            # 文字
            board.checked_rows[next_row][next_col] = True  # 移動前の位置をチェック
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

    if board.rows[cur_row][cur_col] in ('↑', '→', '↓', '┌', '└', '│┌', '│└', '└┌', '┌└'):
        # 左を移動禁止とする現在マス
        return False

    next_col = cur_col - 1
    next_row = cur_row

    if next_col > 0 and next_col < len(board.checked_rows[next_row]) and not board.checked_rows[next_row][next_col]:
        if board.rows[next_row][next_col] in ('┌', '└', '┌r', '└r',
                                              '─', '─┌', '┐─', '┘─', '─└', '└┌', '┌└'):
            # 道
            board.checked_rows[next_row][next_col] = True  # 移動前の位置をチェック
            agent.location[0] -= 1
            return True

        if len(board.rows[next_row][next_col]) == 1 or board.rows[next_row][next_col] == '..':
            # 文字
            board.checked_rows[next_row][next_col] = True  # 移動前の位置をチェック
            agent.location[0] -= 1
            return True

    return False


def undo_move_to_left(agent):
    """←左に移動しなかったことにする"""
    agent.location[0] += 1
