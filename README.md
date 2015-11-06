# chunchun
南ことりが日の出をお知らせします♪

## このスクリプトについて
動かしておくと毎日日の出の時間に南ことりがTwitterに日の出のお知らせをPostします。
南ことり？誰？という人はラブライブ！のBD全部観てCD全部聴け。話は以上だ。

## 動作環境
Python 2.7.xで動きます。我が家ではUbuntu14.04LTSで稼働しています。
request_oauthlibとAPSchedulerに依存しています。pipでどうぞ。

## 使い方
conf.json.exampleをconf.jsonにリネームして、各自取得したTwitterのAPIキーと、日の出時刻を取得する位置の座標を入力してください。
あとはコンソールで`./chunchun.py`とかやってもらえれば。

## その他
日の出時刻の取得には農研機構のWebAPIを使用しています。
