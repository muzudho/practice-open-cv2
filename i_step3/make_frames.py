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
    undo_move_up, undo_move_to_right, undo_move_down, undo_move_to_left
from drawing import draw_board, draw_agent


def search(seq, board, agent):
    """描画と探索
    Parameters
    ----------
    agent : Agent
        移動してるやつ
    """

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

    dead_end = True

    # 上に行く
    if move_up(board, agent):
        dead_end = False
        seq, dead_end2 = search(seq, board, agent)
        if dead_end2:
            # どの方向にも行けなかった。移動前の位置をチェック（行き止まりから飛ぶんで）
            board.checked_rows[agent.location[1]][agent.location[0]] = True
        # 戻る
        undo_move_up(agent)

    # 右に行く
    if move_to_right(board, agent):
        dead_end = False
        seq, dead_end2 = search(seq, board, agent)
        if dead_end2:
            # どの方向にも行けなかった。移動前の位置をチェック（行き止まりから飛ぶんで）
            board.checked_rows[agent.location[1]][agent.location[0]] = True
        # 戻る
        undo_move_to_right(agent)

    # 下に行く
    if move_down(board, agent):
        dead_end = False
        seq, dead_end2 = search(seq, board, agent)
        if dead_end2:
            # どの方向にも行けなかった。移動前の位置をチェック（行き止まりから飛ぶんで）
            board.checked_rows[agent.location[1]][agent.location[0]] = True
        # 戻る
        undo_move_down(agent)

    # 左に行く
    if move_to_left(board, agent):
        dead_end = False
        seq, dead_end2 = search(seq, board, agent)
        if dead_end2:
            # どの方向にも行けなかった。移動前の位置をチェック（行き止まりから飛ぶんで）
            board.checked_rows[agent.location[1]][agent.location[0]] = True
        # 戻る
        undo_move_to_left(agent)

    #cv2.imshow("make_image.py", canvas)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return seq, dead_end


BOARD1 = read_screen_csv(FILE_PATH)
AGENT1 = Agent()
AGENT1.location = BOARD1.start_location
AGENT1.prev_location = BOARD1.start_location

# for (row, columns) in enumerate(BOARD1.rows):
#    for (column, cell) in enumerate(columns):
#        print(f"[{column},{row}]={cell}")

SEQ = 0
search(SEQ, BOARD1, AGENT1)
