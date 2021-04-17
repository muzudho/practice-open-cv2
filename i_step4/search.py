"""探索部
"""

from agent_move import move_up, move_to_right, move_down, move_to_left, \
    can_move_up, can_move_to_right, can_move_down, can_move_to_left, \
    undo_move_up, undo_move_to_right, undo_move_down, undo_move_to_left


def search(seq, board, agent, prev_location, screenshot_func):
    """描画と探索
    Parameters
    ----------
    agent : Agent
        移動してるやつ

    Returns
    -------
    seq: int
        画像番号
    """

    # 前向き探索のスクリーンショット
    seq = screenshot_func(seq, board, agent)

    # 前向き探索中の現在位置をチェック
    board.checked_table[agent.location[1]][agent.location[0]] = 'f'

    before_move_location = agent.location[:]  # Copy

    # 進める方角チェック
    well_move_up = can_move_up(board, agent, prev_location)
    well_move_to_right = can_move_to_right(board, agent, prev_location)
    well_move_down = can_move_down(board, agent, prev_location)
    well_move_to_left = can_move_to_left(board, agent, prev_location)

    # 行き止まりなら
    if not well_move_up and not well_move_to_right and not well_move_down and not well_move_to_left:
        # 後ろ向き探索中の現在位置をチェック
        board.checked_table[agent.location[1]][agent.location[0]] = 'b'
        return seq

    # 上に行く
    if well_move_up:
        move_up(agent)
        if before_move_location[0] == agent.location[0] and \
                before_move_location[1] == agent.location[1]:
            raise Exception(f"move_up失敗")
        seq = search(seq, board, agent, before_move_location, screenshot_func)
        # 戻る
        undo_move_up(agent)
        # 後ろ向き探索のスクリーンショット
        seq = screenshot_func(seq, board, agent, screenshot_func)
        # 後ろ向き探索中の現在位置をチェック
        board.checked_table[agent.location[1]][agent.location[0]] = 'b'

    # 右に行く
    if well_move_to_right:
        move_to_right(agent)
        if before_move_location[0] == agent.location[0] and \
                before_move_location[1] == agent.location[1]:
            raise Exception(f"move_to_right失敗")
        seq = search(seq, board, agent, before_move_location, screenshot_func)
        # 戻る
        undo_move_to_right(agent)
        # 後ろ向き探索のスクリーンショット
        seq = screenshot_func(seq, board, agent)
        # 後ろ向き探索中の現在位置をチェック
        board.checked_table[agent.location[1]][agent.location[0]] = 'b'

    # 下に行く
    if well_move_down:
        move_down(agent)
        if before_move_location[0] == agent.location[0] and \
                before_move_location[1] == agent.location[1]:
            raise Exception(f"move_down失敗")
        seq = search(seq, board, agent, before_move_location, screenshot_func)
        # 戻る
        undo_move_down(agent)
        # 後ろ向き探索のスクリーンショット
        seq = screenshot_func(seq, board, agent)
        # 後ろ向き探索中の現在位置をチェック
        board.checked_table[agent.location[1]][agent.location[0]] = 'b'

    # 左に行く
    if well_move_to_left:
        move_to_left(agent)
        if before_move_location[0] == agent.location[0] and \
                before_move_location[1] == agent.location[1]:
            raise Exception(f"move_to_left失敗")
        seq = search(seq, board, agent, before_move_location, screenshot_func)
        # 戻る
        undo_move_to_left(agent)
        # 後ろ向き探索のスクリーンショット
        seq = screenshot_func(seq, board, agent)
        # 後ろ向き探索中の現在位置をチェック
        board.checked_table[agent.location[1]][agent.location[0]] = 'b'

    #cv2.imshow("make_image.py", canvas)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return seq
