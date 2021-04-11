# practice-open-cv2

![20210411color65_c_step28.gif](./@doc/c_step/img/20210411color65_c_step28.gif)  
(上図は ⚡📄`c_step28/make_frames.py` と ⚡📄`e_step4/pygame00.py` 使用)  

## HULビューモデルって何？

ざっくり言うと HSVモデルを図形で説明（View）する試みの１つで、それに失敗したのが HULビューモデル。  

## HSVモデルと、HULビューモデルの同じところ

* (1) HSVモデルの `H` は、 HULモデルも同じ `H`。  
* (2) HSVモデルの `S` は、 HULモデルの `U - L` 。  
* (3) HSVモデルの `V` は、 HULモデルも同じで、呼び方だけ違う `U` 。  

### (1)

RGB値の比で 色相環の角度、Hue(H) を表す。  
HULモデルは それと同じことを 円に内接する正三角形の回転という別の言い回しで説明しているだけ。  

### (2)

HSVモデルは 彩度(S) で表す。  
HULモデルは それと同じことを 上限値(U) - 下限値(L) で表す。  

### (3)

HSVモデルは 明度(V) で表す。  
HULモデルは それと同じことを RGB値のバーの 上限値(U) という別の言い回しで説明しているだけ。  

## HSVモデルと、HULモデルの違うところ

HSVモデルの精度が 実数 なのに対し、 HULモデルの精度は 弧度法の整数部の0を含む自然数 0～365 （精度の劣化）。

## HULモデルのソースの使い方

GPLライセンスのライブラリが含まれてるから、プログラムは個別にライブラリのライセンスを要確認（＾～＾）  
HULモデルはアルゴリズムなんで 著作権無いんで理解したら独自実装し直して持ってけだぜ（＾～＾）  

* 📁`c_step28` - わたしの考えたHULモデルのエキシビジョン（＾～＾）
  * 📄`make_frames.py` - 実行しろだぜ（＾～＾）1フレームごとの画像ファイルを 📁`shared` に大量に作るぜ（＾～＾）
  * ⚙️📄`conf.py` - いろいろな設定
  * ⚡📄`color_hul_model.py` - わたしのHULモデルをGPLで実装したやつ（＾～＾） ソースはGPLで使いにくいだろうから、それが嫌なやつはアルゴリズムだけ理解して自力実装し直せだぜ（＾～＾）
* 📁`e_step4` - c_step28で作った1フレームごとの画像を紙芝居にして動画で流すやつ。
  * ⚡📄`pygame00.py` - `FRAME_COUNT` グローバル変数を出力された画像の枚数に設定しろだぜ（＾～＾） 実行しろだぜ（＾～＾）
* 📁`shared` - c_step28 を実行したら、画像が大量に出力されるぜ（＾～＾）

## Set up

```shell
pip install opencv-python
pip install pylint
python -m pylint --generate-rcfile > pylintrc

python -m pip install -U pygame --user

# 注意！ 音が出るゲーム画面が出る
python -m pygame.examples.aliens
```

VSCode `[File] - [Preferences] - [Settings]`。 検索欄に `Python.linting.pylintArgs` を入れて検索。 `--extension-pkg-whitelist=cv2,pygame` を追加。  

## Start

```shell
cd c_step28

python make_frame.py

cd e_step4

python pygame00.py
```

## c_step28 図解

![20210411color61a5a1_c_step_28.png](./@doc/c_step/img/20210411color61a5a1_c_step_28.png)
## Document

[References](./@doc/references.md)  
