"""パーサー図。
ただの方眼紙とします"""

import cv2
import numpy as np
from cv2_helper import color_for_cv2
from conf import CANVAS_CHANNELS, GRID_UNIT, FILE_PATH
from conf2 import BACKGROUND_COLOR
from board import read_screen_csv
from agent import Agent
from agent_move import move_up, move_to_right, move_down, move_to_left, \
    can_move_up, can_move_to_right, can_move_down, can_move_to_left, \
    undo_move_up, undo_move_to_right, undo_move_down, undo_move_to_left
from drawing import draw_board, draw_agent


def screenshot(seq, board, agent):
    # キャンバス生成
    canvas = np.full((board.height*GRID_UNIT, board.width*GRID_UNIT, CANVAS_CHANNELS),
                     color_for_cv2(BACKGROUND_COLOR)[0], dtype=np.uint8)

    # 盤の描画
    draw_board(canvas, board)

    # エージェントの描画
    draw_agent(canvas, agent)

    # 書出し
    canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)  # BGRをRGBにする
    cv2.imwrite(f"./@share/out-istep1-{seq}.png", canvas)
    seq += 1

    return seq


def search(seq, board, agent, prev_location):
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
    seq = screenshot(seq, board, agent)

    # 現在位置をチェック
    board.checked_rows[agent.location[1]][agent.location[0]] = True

    before_move_location = agent.location

    # 進める方角チェック
    well_move_up = can_move_up(board, agent, prev_location)
    well_move_to_right = can_move_to_right(board, agent, prev_location)
    well_move_down = can_move_down(board, agent, prev_location)
    well_move_to_left = can_move_to_left(board, agent, prev_location)

    # 行き止まりなら
    if not well_move_up and not well_move_to_right and not well_move_down and not well_move_to_left:
        return seq

    # 上に行く
    if well_move_up:
        move_up(agent)
        seq = search(seq, board, agent, before_move_location)
        # 戻る
        undo_move_up(agent)
        # 後ろ向き探索のスクリーンショット
        seq = screenshot(seq, board, agent)

    # 右に行く
    if well_move_to_right:
        move_to_right(agent)
        seq = search(seq, board, agent, before_move_location)
        # 戻る
        undo_move_to_right(agent)
        # 後ろ向き探索のスクリーンショット
        seq = screenshot(seq, board, agent)

    # 下に行く
    if well_move_down:
        move_down(agent)
        seq = search(seq, board, agent, before_move_location)
        # 戻る
        undo_move_down(agent)
        # 後ろ向き探索のスクリーンショット
        seq = screenshot(seq, board, agent)

    # 左に行く
    if well_move_to_left:
        move_to_left(agent)
        seq = search(seq, board, agent, before_move_location)
        # 戻る
        undo_move_to_left(agent)
        # 後ろ向き探索のスクリーンショット
        seq = screenshot(seq, board, agent)

    #cv2.imshow("make_image.py", canvas)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return seq


BOARD1 = read_screen_csv(FILE_PATH)
AGENT1 = Agent()
AGENT1.location = BOARD1.start_location
AGENT1.prev_location = BOARD1.start_location

# for (row, columns) in enumerate(BOARD1.rows):
#    for (column, cell) in enumerate(columns):
#        print(f"[{column},{row}]={cell}")

SEQ = 0
search(SEQ, BOARD1, AGENT1, AGENT1.location)
