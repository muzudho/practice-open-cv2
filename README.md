# practice-open-cv2

GPLライセンスのライブラリが含まれてるから、プログラムは個別にライブラリのライセンスを要確認（＾～＾）  
HULモデルはアルゴリズムなんで 著作権無いんで理解したら独自実装し直して持ってけだぜ（＾～＾）  

* 📁`c_step24` - わたしのHULモデルをGPLで実装したやつ（＾～＾） ソースではなくアルゴリズムだけ持ってけだぜ（＾～＾）1フレームごとの画像ファイルを大量に作るぜ（＾～＾）
* 📁`e_step4` - c_step24で作った1フレームごとの画像を紙芝居にして動画で流すやつ。画像のメモリ展開のために１分ぐらい真っ暗な画面で待たされろだぜ（＾～＾）
* 📁`shared` - c_step24 を実行したら、画像が4560枚ぐらい出力されるぜ（＾～＾）

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
cd c_step23

python make_frame.py

cd e_step4

python pygame00.py
```

## Document

[References](./@doc/references.md)  
