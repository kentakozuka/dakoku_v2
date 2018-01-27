import mysql.connector
import const

class Handler:
    ''' ハンドラー親クラス '''

    def __init__(self, message):
        self.message = message
        self.connect = self.connect_db()
        self.cursor = self.create_cursor(self.connect)

    def connect_db(self):
        # connect
        return mysql.connector.connect( \
                                host=const.DB_HOST \
                            ,   port=const.DB_PORT \
                            ,   user=const.DB_USER \
                            ,   password=const.DB_PASSWORD \
                            ,   database=const.DB_DATABASE \
                            ,   charset='utf8')


    def create_cursor(self, connect):
        ''' create cursor with dictionary option'''
        return connect.cursor(dictionary=True)

    def get_message_body(self):
        ''' メッセージを取得'''
        return self.message.body['text']

    def get_user_info(self, slack_user_name):
        ''' ユーザー情報を取得 '''
        select_query =  ('SELECT * FROM user LEFT JOIN office ON user.office_pk=office.id WHERE user.slack_user_name = %(slack_user_name)s')
        self.cursor.execute(select_query, ({'slack_user_name': slack_user_name}))
        return self.cursor.fetchone()

    def is_all_fields_filled(self, slack_user_name):
        ''' すべての項目に値が入っているか確認する '''
        user_info = self.get_user_info(slack_user_name)
        for k in user_info.keys():
            if user_info[k] is None:
                return False
        return True

    def get_send_user(self):
        '''ユーザ名の取得'''
        return self.message.channel._client.users[self.message.body['user']]['name']

    def get_channel_info(self):
        '''チャンネル情報の取得'''
        return self.message.channel._client.channels[self.message.body['channel']]

    def get_version_info(self):
        '''バージョン情報の取得'''
        return const.VERSION_INFO

    def execute_query(self, query, params):
        '''クエリを実行する'''
        try:
            self.cursor.execute(query, params)

        except Exception as e:
            self.connect.rollback()
            print(e)
            raise e

        finally:
            pass

    def commit(self):
        '''コミットする'''
        self.connect.commit()

    def close_cursor(self):
        '''cursorを閉じる'''
        self.cursor.close()

    def close_connection(self):
        '''接続を閉じる'''
        self.connect.close()

