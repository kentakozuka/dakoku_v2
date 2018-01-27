from slacker import Slacker

import chardet
import json
import os

import sys
sys.path.append("./plugins/")
import const
import timestamp as Ts
from handler import Handler

class MessageHandler(Handler):
    '''メッセージハンドリングクラス'''

    def __init__(self, message, crawlrunner, finish_msg, greeting_msg):
        super().__init__(message)
        self.message = message
        self.crawlrunner = crawlrunner
        self.finish_msg = finish_msg
        self.greeting_msg = greeting_msg

        curpath = (os.path.dirname(__file__))
        self.fpath = curpath + const.FPATH
        self.version_info = super().get_version_info()

    def run_crawler(self):
        ''' クロール共通処理 '''
        # ユーザー名を取得
        send_user = self.get_send_user()
        user_info = super().get_user_info(send_user)

        # チャンネル名を取得
        channel_info = self.get_channel_info()

        # ユーザー情報が存在すれば打刻処理を行う
        if user_info:
            if not super().is_all_fields_filled(send_user):
                self.message.reply('設定されていない項目があるため打刻処理を実行できません。')
            else:
                # クロール
                img_path = self.crawlrunner.run(user_info)
                # スクショを投稿
                self.post_img(img_path)
        else:
            self.message.reply(self.greeting_msg.format(send_user))

        # disconnect
        self.cursor.close()
        self.connect.close()

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
