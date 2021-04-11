# practice-open-cv2

![20210411color65_c_step28.gif](./@doc/c_step/img/20210411color65_c_step28.gif)  
(上図は ⚡📄`c_step28/make_frames.py` と ⚡📄`e_step4/pygame00.py` 使用)  

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
