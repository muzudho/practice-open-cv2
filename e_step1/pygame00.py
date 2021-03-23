# coding: utf -8

# モジュールの読み込み
import sys
import pygame
from pygame.locals import QUIT

# pygame の初期化
pygame.init()

w = 400
h = 300
sf = pygame.display.set_mode((w, h))  # アプリケーションウィンドウ
pygame.display.set_caption('Application: pygame00.py')

fps = pygame.time.Clock()  # フレームレート制御のための Clock オブジェクト

# 画像の読み込み
im1 = pygame.image.load('./e_step1/img/ball01.png')
im1_w = im1.get_width()  # 画像の横幅の取得
im1_h = im1.get_height()  # 画像の高さの取得

# メインループ
x = 0
y = 0  # ボールの位置
dx = 3
dy = 2  # 移動量
while True:
    sf.fill((255, 255, 255))  # 背景の色
    sf.blit(im1, (x, y))  # ボールの描画
    # イベントキューを処理するループ
    for ev in pygame.event.get():

        if ev.type == QUIT:  # 「終了」イベント
            pygame.quit()
            print('quitting...')
            sys.exit()
    # ディスプレイの更新
    pygame.display.update()
    # フレームレートの設定
    fps.tick(30)  # 30 FPS に設定
    # ボール移動（位置変更）の処理
    x += dx
    y += dy  # 移 動
    if x + im1_w > w:  # ボールが右端に衝突した場合の処理
        x = w - im1_w - 1
        dx *= -1
    elif x < 0:  # ボールが左端に衝突した場合の処理
        x = 0
        dx *= -1
    if y + im1_h > h:  # ボールが床に衝突した場合の処理
        y = h - im1_h - 1
        dy *= -1
    elif y < 0:  # ボールが天井に衝突した場合の処理
        y = 0
        dy *= -1
