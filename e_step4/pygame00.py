"""coding: utf -8
"""

# モジュールの読み込み
import sys
import time
import pygame
from pygame.locals import QUIT

# pygame の初期化
pygame.init()

# 画像の読み込み
FRAME_COUNT = 72
IMAGE1 = pygame.image.load('./shared/out-cstep4-0.png')
IMAGE1_W = IMAGE1.get_width()  # 画像の横幅の取得
IMAGE1_H = IMAGE1.get_height()  # 画像の高さの取得

DISPLAY_SIZE = (IMAGE1_W, IMAGE1_H)  # width, height
SURFACE = pygame.display.set_mode(DISPLAY_SIZE)  # アプリケーションウィンドウ
pygame.display.set_caption('Application: pygame00.py')

CLOCK = pygame.time.Clock()  # フレームレート制御のための Clock オブジェクト

# 画像の先読み
FRAMES = []
for i in range(0, FRAME_COUNT):
    IMAGE1 = pygame.image.load(f'./shared/out-cstep4-{i}.png')
    FRAMES.append(IMAGE1)


# メインループ
WHITE = (255, 255, 255)
BALLP = [0, 0]  # x, y
DX = 3
DY = 2  # 移動量
for j in range(0, 2):  # 2ループ
    for i in range(0, FRAME_COUNT):
        # SURFACE.fill(WHITE)  # 背景の色
        SURFACE.blit(FRAMES[i], (BALLP[0], BALLP[1]))  # ボールの描画

        # イベントキューを処理するループ
        for ev in pygame.event.get():

            if ev.type == QUIT:  # 「終了」イベント
                pygame.quit()
                print('quitting...')
                sys.exit()

        # ディスプレイの更新
        pygame.display.update()

        if j == 0 and i == 0:
            time.sleep(3)  # Seconds

        # フレームレートの設定
        CLOCK.tick(9)  # fps を指定

time.sleep(3)  # Seconds
