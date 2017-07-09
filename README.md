# tenki

## Description
tenki.jpから天気を取得してターミナルに表示します。

## Demo
<img src="demo/demo1.png" alt="ターミナル上での表示" style="max-width:50%"><br>
ターミナル上での表示

<img src="demo/demo2.png" alt="ターミナル上での表示(urlを指定)" style="max-width:50%"><br>
ターミナル上での表示(URLを指定して札幌市の天気を表示)

<img src="demo/demo3.png" alt="conkyでの表示" style="max-width:50%"><br>
conkyでの表示

## Requirements
- python 2
- [click](http://click.pocoo.org)
- [lxml](http://lxml.de)

## Installation
click, lxmlがインストールされていない場合はインストールしてください。
```
$ sudo pip install click
$ sudo pip install lxml
```

## Usage
```
$ ./tenki.py  # デフォルトではつくば市の天気が表示されます。
```

`--url`でtenki.jpの任意の地点の3時間天気のページのURLを指定することで、その地点の天気を表示できます。
```
$ ./tenki.py --url https://tenki.jp/forecast/3/16/4410/13101/3hours.html  # 東京都千代田区の天気を表示
```




---

`--conky`オプションを付けると、出力がconky用になります。
conkyで使う場合は.conkyrcに以下を追記します。
```
${execp [tenki.pyのパス] --conky}
```


## Licence
- MIT


## Auther
[algon-320](https://github.com/algon-320)
