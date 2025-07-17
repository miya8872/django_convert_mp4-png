# 動画->画像変換Webアプリ
動画をWebサイトから受け取り、フレーム差違を抽出した上で、それら差異を順に重ねた画像を出力します。

例：動画 -> 画像  
※ 動画はGIFに変換済みであり以下はイメージです
<table>
  <tr>
    <td><img src="https://raw.githubusercontent.com/miya8872/django_convert_mp4-png/refs/heads/master/example/example.gif" width="300"></td>
    <td><img src="https://raw.githubusercontent.com/miya8872/django_convert_mp4-png/refs/heads/master/example/example.png" width="300"></td>
  </tr>
</table>

また、本サイトはAWSのEC2にてデプロイしており、  
AWSやWebサイトのバックエンド処理の学習目的で作成いたしました。

## 機能概要
・フレーム間の差異の抽出と合成  
・4桁のPINコードでの保護  
・プログレスの表示
・画像のバイナリ化と送受信  
・古いファイルの定期的な削除機能  
・同時に処理するファイル数の制限

## 使用技術
・django を用いたルーティングとリクエスト処理  
・OpenCV を用いた動画の画像化と画像処理  
・apscheduler.schedulers.background を用いた定期的な関数の実行  
・AWS EC2 を用いたインスタンスの作成及び使用  
・Gunicorn を用いたWSGIサーバーの作成及び使用  
・Nginx を用いた静的ファイルの配信やHttps対応、入力ファイルのサイズ制限(25MB)

## 設計上の工夫点
・最低限Webアプリケーションとして、継続して機能することを意識して作成しました  
・上記の一環としてメディアを直URLで配信することは避け、fetchAPIとpythonを組み合わせての配信としています  
・画像処理に時間がかかってしまうため、使用者視点だと必要なプログレス表示を実装しています

## 今後の課題
・例外処理やログに関しての実装がほぼないため、継続利用にはそれらの実装が必須である点  
・PINの認証時にCookieを使用しているにも関わらず自動認証を実装していない点
・画像生成にはパラメータを用意しているが、それらがサイトから操作不能である点
・外見は度外視で作成したため、それらの改善

## 開発/動作環境
Windows10 home  
Python 3.10.11  
Library requirement.txtに記載  

ubuntu-jammy-22.04-amd64-server-20250516  
Python 3.10.12  
nginx 1.18.0  
gunicorn 23.0.0  
package package.txtに記載

## ライセンス
これらソースコードはポートフォリオ用に公開しています。  
動作に関しても保証しかねるため、以下の利用を禁止といたします。  
商用利用 二次利用 再配布

ただし、応募企業様が企業内で共有する場合に限り、再配布可といたします。
