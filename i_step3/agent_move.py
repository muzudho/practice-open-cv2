"""エージェントの移動
"""


def move_up(_board, agent):
    """上に移動"""
    if agent.location[1] > 0:
        agent.location[1] -= 1
        return True
    return False


def move_to_right(board, agent):
    """右に移動"""
    if agent.location[0] + 1 < board.width:
        agent.location[0] += 1
        return True
    return False


def move_down(board, agent):
    """下に移動"""
    if agent.location[1] + 1 < board.height:
        agent.location[1] += 1
        return True
    return False


def move_to_left(_board, agent):
    """左に移動"""
    if agent.location[0] > 0:
        agent.location[0] -= 1
        return True
    return False
