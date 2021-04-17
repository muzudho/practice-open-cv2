"""エージェントの移動
"""


def move_up(board, agent):
    """↑上に移動"""
    column = agent.location[0]
    row = agent.location[1] - 1
    if row >= 0 and not board.checked_rows[row][column] \
            and board.rows[row][column] in ('┌', '┐', '│', '│┌', '┐│', '┘│', '│└', '┐┌'):
        board.checked_rows[row][column] = True
        agent.location[1] -= 1
        return True
    return False


def undo_move_up(agent):
    """↑上に移動しなかったことにする"""
    agent.location[1] += 1


def move_to_right(board, agent):
    """→右に移動"""
    column = agent.location[0] + 1
    row = agent.location[1]
    if column < board.width and not board.checked_rows[row][column] \
            and board.rows[row][column] in ('┐', '┘', '─', '─┌', '┐─', '┘─', '─└', '┘┐', '┐┘'):
        board.checked_rows[row][column] = True
        agent.location[0] += 1
        return True
    return False


def undo_move_to_right(agent):
    """→右に移動しなかったことにする"""
    agent.location[0] -= 1


def move_down(board, agent):
    """↓下に移動"""
    column = agent.location[0]
    row = agent.location[1] + 1
    if row < board.height and not board.checked_rows[row][column] \
            and board.rows[row][column] in ('┘', '└', '│', '│┌', '┐│', '┘│', '│└', '┘└'):
        board.checked_rows[row][column] = True
        agent.location[1] += 1
        return True
    return False


def undo_move_down(agent):
    """↓下に移動しなかったことにする"""
    agent.location[1] -= 1


def move_to_left(board, agent):
    """←左に移動"""
    column = agent.location[0] - 1
    row = agent.location[1]
    if column > 0 and not board.checked_rows[row][column] \
            and board.rows[row][column] in ('┌', '└', '─', '─┌', '┐─', '┘─', '─└', '└┌', '┌└'):
        board.checked_rows[row][column] = True
        agent.location[0] -= 1
        return True
    return False


def undo_move_to_left(agent):
    """←左に移動しなかったことにする"""
    agent.location[0] += 1
