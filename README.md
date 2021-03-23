# practice-open-cv2

gifアニメ作成の練習（＾～＾）


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

## References

* a
  * [【python/OpenCV/Pillow】Pillowを使ってgifアニメーションを作成してみる](https://rikoubou.hatenablog.com/entry/2020/04/03/151906) - 読んでも分からない（＾～＾）インデックス・パレット使ってる（＾～＾）
* b
  * [python : gifの作成（アニメーション）](https://kangkang1981.hatenablog.com/entry/2020/03/19/224219)
* Python Library
  * [Python3ライブラリブック](https://ktechlabo.xsrv.jp/www_python/python_modules.pdf)
* OpenCV2
  * [OpenCVをVisual Studio Codeで使う時にcv2モジュールのインテリセンスが表示されない問題](https://qiita.com/FXsimone/items/577e3924f40aa4a9d4ea)
* pylint
  * [pylintでコードチェックをしたいが，そもそも実行エラーが出てしまう．](https://teratail.com/questions/197652)
