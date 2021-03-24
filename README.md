# practice-open-cv2

gifアニメ作成の練習（＾～＾）

* `c_step7` - ぐるぐる回るカラーパレットの連続写真を取るやつ
* `e_step4` - 紙芝居を動画で流すやつ
* `f_step1` - 数学ライブラリを試すやつ

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
cd b_step1

python make_gif.py
```

## Document

[References](./@doc/references.md)  
