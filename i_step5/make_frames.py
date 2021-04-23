"""パーサー図。
ただの方眼紙とします"""

import cv2
import numpy as np
from cv2_helper import color_for_cv2
from conf import CANVAS_CHANNELS, GRID_UNIT, FILE_PATH
from conf2 import BACKGROUND_COLOR
from board import read_screen_csv
from agent import Agent
from drawing import draw_board, draw_agent
from search import search


def screenshot_func(seq, board, agent):
    """画像を出力します"""
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


BOARD1 = read_screen_csv(FILE_PATH)
AGENT1 = Agent()
AGENT1.location = BOARD1.start_location[:]  # Copy
AGENT1.prev_location = BOARD1.start_location[:]  # Copy

# for (row, columns) in enumerate(BOARD1.rows):
#    for (column, cell) in enumerate(columns):
#        print(f"[{column},{row}]={cell}")

print("Start...")

SEQ1 = 0
SEQ1 = search(SEQ1, BOARD1, AGENT1, AGENT1.location, screenshot_func)
# 後ろ向き探索のスクリーンショット
screenshot_func(SEQ1, BOARD1, AGENT1)

print("Finished.")
