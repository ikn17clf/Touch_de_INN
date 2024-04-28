私が所属するサークルの部室入り口に，Suicaなどの交通系ICカードで部室の鍵を解錠するシステムを導入しようとした時のプログラム<br>
仕組みは以下の通り

1. サークルの会員のユーザとICカードの情報を登録するデータベースとして，サークルの管理用Googleアカウント上に用意したGoogleスプレッドシートを用いる．
2. memberlist_download.py，及び，touch_de_inn_3.py は，NFCタグを接続したラズベリーパイ上で常時動かす<br>
   memberlist_download.py は，データベースたるGoogleスプレッドシートを一定時間ごとにダウンロードしてcsvファイルとしてラズパイの中に保存するプログラム<br>
   touch_de_inn_3.py は，NFCタグで読み取った情報がcsvファイル上に存在するかどうかを判定するプログラム<br>
   本当は解錠も実装したかったけど，当時は物理的な障壁があり断念<br>
   SwitchBot ロック( https://www.switchbot.jp/products/switchbot-lock )とIFTTTを使えば実装できるかも
3. touch_de_inn_admin_app.py は，ユーザとICカード情報をGoogleスプレッドシートに登録するGUIアプリ<br>
   NFCタグを接続したWindowsマシンで使うことを想定している
   
NB: NFCタグは最新のものだとカードの情報が読み取れないので，古いバージョンのものを使う必要がある．<br>
    GoogleスプレッドシートをPythonで読み込む方法は以下を参照<br>
    https://programmer-life.work/python/read-spreadsheet-data
    <br>GoogleスプレッドシートをPythonで読み込む前に，認証用のjsonファイルを同じディレクトリに置いておく必要がある．その方法は以下を参照<br>
    https://programmer-life.work/python/python-to-google-spreadsheet
