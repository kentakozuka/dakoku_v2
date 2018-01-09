from slacker import Slacker

import chardet
import json
import os

# 定数モジュール
import sys
sys.path.append("./plugins/")
import const
import timestamp as Ts

class MessageHandler():
    '''メッセージハンドリングクラス'''

    def __init__(self, message, crawlrunner, finish_msg, greeting_msg):
        self.message = message
        self.crawlrunner = crawlrunner
        self.finish_msg = finish_msg
        self.greeting_msg = greeting_msg

        self.version_info = self.get_version_info

        curpath = (os.path.dirname(__file__))
        self.fpath = curpath + const.FPATH
        self.version_info = self.get_version_info()

    def run_crawler(self):
        ''' クロール共通処理 '''
        # ユーザー名を取得
        send_user = self.get_send_user()
        user_info = self.get_user_info(send_user)

        # チャンネル名を取得
        channel_info = self.get_channel_info()

        # ユーザー情報が存在すれば打刻処理を行う
        if user_info:
            # クロール
            img_path = self.crawlrunner.run(user_info)
            # スクショを投稿
            self.post_img(img_path)
        else:
            self.message.reply(self.greeting_msg.format(send_user))

    def get_user_info(self, su):
        ''' ユーザー情報を取得 '''
        # jsonファイルを読み込む
        f = open(self.fpath, encoding='utf-8')
        d = json.load(f)
        f.close()
        return [d[i] for i in range(len(d)) if d[i]["slack_user_name"] == su][0]

    def get_send_user(self):
        '''ユーザ名の取得'''
        return self.message.channel._client.users[self.message.body['user']]['name']

    def get_channel_info(self):
        '''チャンネル情報の取得'''
        return self.message.channel._client.channels[self.message.body['channel']]

    def get_version_info(self):
        '''バージョン情報の取得'''
        return const.VERSION_INFO

    def post_img(self, file_path):
        ''' スクショを投稿する '''
        # 投稿するチャンネル名
        c_name = self.get_channel_info()['name']
        # 投稿
        slacker = Slacker(const.API_TOKEN)
        slacker.files.upload( \
                    file_path, \
                    channels=[c_name], \
                    title=self.finish_msg.format(self.get_send_user(), self.version_info))
