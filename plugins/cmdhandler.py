import os
import copy

import mysql.connector

from handler import Handler
from dakokuparser import DakokuParser
import const

class CommandHandler(Handler):
    '''コマンドハンドリングクラス'''

    def __init__(self, message):
        super().__init__(message)
        self.msg = ''

    def get_msg(self):
        result = self.get_parse_result()

        # 不正なコマンド
        if not result.is_success:
            self.msg = result.msg + '\n' + self.wrap_triple_backquots(self.get_usage())
            return self.msg

        self.exec_command(result)
        return self.msg

    def exec_command(self, result):
        '''  '''
        # show user command
        if result.ret_val == const.RET_VAL_SHOW_USER:
            self.show_user(super().get_send_user())
            return

        # show office command
        if result.ret_val == const.RET_VAL_SHOW_OFFICE:
            self.show_office()
            return

        # add command
        if result.ret_val == const.RET_VAL_ADD:
            self.add_user(super().get_send_user())
            return

        # del command
        if result.ret_val == const.RET_VAL_DEL:
            self.delete_user(super().get_send_user())
            return

        # set command
        self.set_vals(super().get_send_user(), result.ret_val)

    def show_user(self, slack_user_name):
        query =  ('''
                    SELECT
                          slack_user_name
                        , daim_id
                        , daim_password
                        , office_pk
                        , office_name
                        , department
                        , next_department
                        , start_hour
                        , start_min
                        , leave_hour
                        , leave_min
                        , overtime_cause
                    FROM user
                    LEFT JOIN office ON user.office_pk=office.id
                    WHERE user.slack_user_name = %(slack_user_name)s
                  ''')
        params = ({'slack_user_name': slack_user_name})

        try:
            super().execute_query(query, params)
            row = self.cursor.fetchone()
            if self.cursor.rowcount < 0:
                self.msg = 'no user'
            else:
                for k in row.keys():
                    ostr = ''
                    if row[k] is None:
                        ostr = '値を設定してください。'
                    else:
                        if k == 'daim_password':
                            ostr = ''.join([ '*' for _ in range(len(row[k]))])
                        else:
                            ostr = str(row[k])
                    self.msg += '\n' + k + ': ' + ostr

        except Exception as e:
            print(e)
            self.connect.rollback()
            self.msg = const.ERRMSG_DML

        finally:
            super().commit()
            super().close_cursor
            super().close_connection

    def show_office(self):
        query =  ('SELECT id, office_name FROM office')
        try:
            super().execute_query(query, None)

            for i in self.cursor:
                self.msg += '\n' + str(i)

            if self.cursor.rowcount < 0:
                self.msg = 'no office'

        except Exception as e:
            self.connect.rollback()
            self.msg = const.ERRMSG_DML

        finally:
            super().commit()
            super().close_cursor
            super().close_connection

    def add_user(self, slack_user_name):
        '''  '''
        query = ("insert into user \
                            ( \
                              slack_user_name \
                            , daim_id \
                            , daim_password \
                            , office_pk \
                            , department \
                            , next_department \
                            , start_hour \
                            , start_min \
                            , leave_hour \
                            , leave_min \
                            , overtime_cause \
                            ) \
                       values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

        params = ( \
                        slack_user_name
                      , None , None , None , '01' , '00'
                      , None , None , None , None , None
                    )

        try:
            super().execute_query(query, params)
            self.msg = 'added!'

        except Exception as e:
            self.connect.rollback()
            self.msg = const.ERRMSG_DML

        finally:
            super().commit()
            super().close_cursor
            super().close_connection

    def delete_user(self, slack_user_name):

        query = 'delete from user where slack_user_name = %(slack_user_name)s'
        params = ({'slack_user_name': slack_user_name})

        try:
            super().execute_query(query, params)
            self.msg = 'deleted!'

        except Exception as e:
            self.connect.rollback()
            self.msg = const.ERRMSG_DML

        finally:
            super().commit()
            super().close_cursor
            super().close_connection

    def set_vals(self, slack_user_name, vals):

        cmd_db_map = {
                      'uid':    'daim_id'
                    , 'pw':     'daim_password'
                    , 'dep':    'office_pk'
                    , 'atime':  'atime'
                    , 'ltime':  'ltime'
                    , 'cow':    'overtime_cause'
                    }

        update_fields = {cmd_db_map[k]: vals[k] for k in vals.keys()}

        # 部署はint
        if 'office_pk' in update_fields:
            update_fields['office_pk'] = int(update_fields['office_pk'])

        # 時を分を分割する
        if 'atime' in update_fields:
            print(update_fields['atime'])
            time_list = update_fields['atime'].split(':')
            print(time_list)
            update_fields['start_hour'] = time_list[0]
            update_fields['start_min'] = time_list[1]
            del update_fields['atime']

        if 'ltime' in update_fields:
            time_list = update_fields['ltime'].split(':')
            update_fields['leave_hour'] = time_list[0]
            update_fields['leave_min'] = time_list[1]
            del update_fields['ltime']

        fields = [k + '=%(' + k + ')s' for k in update_fields]

        query = ' update user set ' + ','.join(fields) + ' where slack_user_name = %(slack_user_name)s'

        params = copy.deepcopy(update_fields)
        params['slack_user_name'] = slack_user_name
        params = (params)

        try:
            super().execute_query(query, params)
            self.msg = 'updated!'

        except Exception as e:
            self.connect.rollback()
            self.msg = const.ERRMSG_DML

        finally:
            super().commit()
            super().close_cursor
            super().close_connection

    def get_parse_result(self):
        ''''''
        dp = DakokuParser(super().get_message_body())
        dp.parse_command()
        return dp

    def wrap_triple_backquots(self, input_str):
        ''''''
        return '```' + input_str + '```'

    def get_usage(self):
        curpath = os.path.dirname(os.path.abspath(__file__))
        fpath = curpath + '/usage.txt'
        f = open(fpath, encoding='utf-8')
        ret_str  = f.read()
        f.close()
        return ret_str

