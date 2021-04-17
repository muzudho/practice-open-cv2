"""エージェントの移動
"""


def move_up(board, agent):
    """↑上に移動"""
    column = agent.location[0]
    row = agent.location[1]

    # 現在マス
    if board.rows[row][column] in ('→', '↓', '←', '┌', '┐', '┘│', '│└', '┐┌', '─┌', '┐─'):
        # 上を移動禁止とする現在マス
        return False

    row -= 1

    if row >= 0 and column < len(board.checked_rows[row]) and not board.checked_rows[row][column]:
        # 次マス
        if board.rows[row][column] in ('┌', '┐', '┌r', '┐r', '│', '│┌', '┐│', '┘│', '│└', '┐┌', '┘┐', '┐┘', '└┌', '┌└'):
            # 道
            board.checked_rows[agent.prev_location[1]
                               ][agent.prev_location[0]] = True  # 移動前の位置をチェック
            agent.prev_location = agent.location
            agent.location[1] -= 1
            return True

        if len(board.rows[row][column]) == 1 or board.rows[row][column] == '..':
            # 文字
            board.checked_rows[agent.prev_location[1]
                               ][agent.prev_location[0]] = True  # 移動前の位置をチェック
            agent.prev_location = agent.location
            agent.location[1] -= 1
            return True

    return False


def undo_move_up(agent):
    """↑上に移動しなかったことにする"""
    agent.prev_location = agent.location
    agent.location[1] += 1


def move_to_right(board, agent):
    """→右に移動"""
    column = agent.location[0] + 1
    row = agent.location[1]

    if board.rows[row][column] in ('↑', '↓', '←', '┐', '┘', '┘│', '┐│', '┘┐', '┐┘'):
        # 右を移動禁止とする現在マス
        return False

    column += 1

    if column < board.width and column < len(board.checked_rows[row]) and not board.checked_rows[row][column]:
        # 道
        if board.rows[row][column] in ('┐', '┘', '┐r', '┘r',
                                       '─', '─┌', '┐─', '┘─', '─└', '┘┐', '┐┘'):
            board.checked_rows[agent.prev_location[1]
                               ][agent.prev_location[0]] = True  # 移動前の位置をチェック
            agent.prev_location = agent.location
            agent.location[0] += 1
            return True

        if len(board.rows[row][column]) == 1 or board.rows[row][column] == '..':
            # 文字
            board.checked_rows[agent.prev_location[1]
                               ][agent.prev_location[0]] = True  # 移動前の位置をチェック
            agent.prev_location = agent.location
            agent.location[0] += 1
            return True

    return False


def undo_move_to_right(agent):
    """→右に移動しなかったことにする"""
    agent.prev_location = agent.location
    agent.location[0] -= 1


def move_down(board, agent):
    """↓下に移動"""
    column = agent.location[0]
    row = agent.location[1]

    if board.rows[row][column] in ('↑', '→', '←', '┘', '└', '─', '┘─', '─└', '┘└'):
        # 下を移動禁止とする現在マス
        return False

    row += 1
    if row < board.height and column < len(board.checked_rows[row]) and not board.checked_rows[row][column]:
        # 道
        if board.rows[row][column] in ('┘', '└', '┘r', '└r', '│', '│┌', '┐│', '┘│', '│└', '┘└', '┘┐', '┐┘', '└┌', '┌└'):
            board.checked_rows[agent.prev_location[1]
                               ][agent.prev_location[0]] = True  # 移動前の位置をチェック
            agent.prev_location = agent.location
            agent.location[1] += 1
            return True

        if len(board.rows[row][column]) == 1 or board.rows[row][column] == '..':
            # 文字
            board.checked_rows[agent.prev_location[1]
                               ][agent.prev_location[0]] = True  # 移動前の位置をチェック
            agent.prev_location = agent.location
            agent.location[1] += 1
            return True

    return False


def undo_move_down(agent):
    """↓下に移動しなかったことにする"""
    agent.prev_location = agent.location
    agent.location[1] -= 1


def move_to_left(board, agent):
    """←左に移動"""
    column = agent.location[0]
    row = agent.location[1]

    if board.rows[row][column] in ('↑', '→', '↓', '┌', '└', '│┌', '│└', '└┌', '┌└'):
        # 左を移動禁止とする現在マス
        return False

    column -= 1

    if column > 0 and column < len(board.checked_rows[row]) and not board.checked_rows[row][column]:
        if board.rows[row][column] in ('┌', '└', '┌r', '└r',
                                       '─', '─┌', '┐─', '┘─', '─└', '└┌', '┌└'):
            # 道
            board.checked_rows[agent.prev_location[1]
                               ][agent.prev_location[0]] = True  # 移動前の位置をチェック
            agent.prev_location = agent.location
            agent.location[0] -= 1
            return True

        if len(board.rows[row][column]) == 1 or board.rows[row][column] == '..':
            # 文字
            board.checked_rows[agent.prev_location[1]
                               ][agent.prev_location[0]] = True  # 移動前の位置をチェック
            agent.prev_location = agent.location
            agent.location[0] -= 1
            return True

    return False


def undo_move_to_left(agent):
    """←左に移動しなかったことにする"""
    agent.prev_location = agent.location
    agent.location[0] += 1
