## tenki

tenki.jp のピンポイント天気を取得して表示します。

### Usage
Python2で動かしてください。

```
$ python ./tenki.py
```

#### conkyに表示させる
`--conky`オプションを付けてtenki.pyを実行すると、conkyに表示するための出力になります。

実際にconkyに表示させるには.conkyrcに以下を追加します。
```
${execp [tenki.pyのパス] --conky}
```

※ フォントの設定によってはうまく表示されないことがあるかもしれません。
