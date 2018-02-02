# 打刻ボット

Slackにメッセージを投稿すると自分の代わりに打刻してくれるボット

## 出勤

「おは」と投稿する。


## 退勤

「おつ」と投稿する。


## 残業申請

「した」と投稿する。

## ユーザー情報登録・変更コマンド

```
使い方: @dakoku_bot コマンド

Slack上で動作する打刻ボット

コマンド:
    show    各種情報を表示します。

            サブコマンド:
                user            ユーザー情報を表示します。
                office          部署情報を表示します。

            入力例 --ユーザー情報を表示する:
                @dakoku_bot show user

    add     ユーザー情報を新規登録します。

            入力例:
                @dakoku_bot add

    set     各種情報を設定します。

            オプション:
                --uid=string    stringにはユーザーID (user id) を入力します。
                --pw=string     stringにはパスワード (password) を入力します。
                --dep=string    stringには所属部署 (department) の番号を入力します。
                --atime=HH:MM   HH:MMには出勤時間 (attendance time) を入力します。
                --ltime=HH:MM   HH:MMには退勤時間 (leaving time) を入力します。
                --cow=string    stringには残業理由 (cause of overtime-work) を入力します。

            入力例 1 --まとめて設定する:
                @dakoku_bot set --uid=0123456789 --pw=mypassword --atime=09:00 --ltime=18:00 --cow=作業過多のため

            入力例 2 --残業理由のみ変更する:
                @dakoku_bot set --cow=作業過多のため

    del     ユーザー情報を削除します。

            入力例:
                @dakoku_bot del

```


## refactoring

* クロールする部分はchain of responsibilityパターンが使えるかも
* ログを実装したい
