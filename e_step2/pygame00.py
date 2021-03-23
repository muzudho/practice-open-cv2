# coding: utf -8

# モジュールの読み込み
import sys
import pygame
from pygame.locals import QUIT

# pygame の初期化
pygame.init()

DISPLAY_SIZE = (400, 300)  # width, height
SURFACE = pygame.display.set_mode(DISPLAY_SIZE)  # アプリケーションウィンドウ
pygame.display.set_caption('Application: pygame00.py')

FPS = pygame.time.Clock()  # フレームレート制御のための Clock オブジェクト

# 画像の読み込み
IMAGE1 = pygame.image.load('./e_step1/img/ball01.png')
IMAGE1_W = IMAGE1.get_width()  # 画像の横幅の取得
IMAGE1_H = IMAGE1.get_height()  # 画像の高さの取得

# メインループ
WHITE = (255, 255, 255)
BALLP = [0, 0]  # x, y
DX = 3
DY = 2  # 移動量
while True:
    SURFACE.fill(WHITE)  # 背景の色
    SURFACE.blit(IMAGE1, (BALLP[0], BALLP[1]))  # ボールの描画
    # イベントキューを処理するループ
    for ev in pygame.event.get():

        if ev.type == QUIT:  # 「終了」イベント
            pygame.quit()
            print('quitting...')
            sys.exit()
    # ディスプレイの更新
    pygame.display.update()
    # フレームレートの設定
    FPS.tick(30)  # 30 FPS に設定
    # ボール移動（位置変更）の処理
    BALLP[0] += DX
    BALLP[1] += DY  # 移 動
    if BALLP[0] + IMAGE1_W > DISPLAY_SIZE[0]:  # ボールが右端に衝突した場合の処理
        BALLP[0] = DISPLAY_SIZE[0] - IMAGE1_W - 1
        DX *= -1
    elif BALLP[0] < 0:  # ボールが左端に衝突した場合の処理
        BALLP[0] = 0
        DX *= -1
    if BALLP[1] + IMAGE1_H > DISPLAY_SIZE[1]:  # ボールが床に衝突した場合の処理
        BALLP[1] = DISPLAY_SIZE[1] - IMAGE1_H - 1
        DY *= -1
    elif BALLP[1] < 0:  # ボールが天井に衝突した場合の処理
        BALLP[1] = 0
        DY *= -1
