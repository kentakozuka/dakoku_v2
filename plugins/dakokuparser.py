import parse # r1chardj0n3s/parse
import time
import const

class DakokuParser():
    ''' コマンドパーサー '''
    def __init__(self, command):
        self.msg =  ''
        self.is_success = False
        self.command = command
        self.ret_val = None

    def parse_command(self):
        ''' コマンドをパースする'''

        r = parse.parse("show {}", self.command)
        if r is not None:
            # err if no sub-command
            if r[0].strip() == '':
                self.msg = const.ERRMSG
                return

            if r[0].strip() == 'user':
                self.is_success = True
                self.ret_val = const.RET_VAL_SHOW_USER
                return

            if r[0].strip() == 'office':
                self.is_success = True
                self.ret_val = const.RET_VAL_SHOW_OFFICE
                return

        if self.command.strip() == 'add':
            self.is_success = True
            self.ret_val = const.RET_VAL_ADD
            return

        if self.command.strip() == 'del':
            self.is_success = True
            self.ret_val = const.RET_VAL_DEL
            return

        r = parse.parse("set {}", self.command)
        if r is not None:
            # err if no options
            if r[0].strip() == '':
                self.msg = const.ERRMSG
                return
            op_dict = self.parse_set(r[0])
            if len(op_dict) == 0:
                return
            else:
                self.is_success = True
                self.ret_val = op_dict
                return

        self.msg = const.ERRMSG

    def parse_set(self, option):
        ''' setコマンドをパースする'''
        op_list = option.split()

        op_dict = {}

        # too many options
        if len(op_list) > 5:
            self.msg = const.ERRMSG
            return

        for o in op_list:

            r = parse.parse('--' + const.PARAM_UID + '={}', o)
            if r is not None:
                op_dict[const.PARAM_UID] = r[0]
                continue

            r = parse.parse('--' + const.PARAM_PW + '={}', o)
            if r is not None:
                op_dict[const.PARAM_PW] = r[0]
                continue

            r = parse.parse('--' + const.PARAM_DEP + '={}', o)
            if r is not None:
                op_dict[const.PARAM_DEP] = r[0]
                continue

            r = parse.parse('--' + const.PARAM_ATIME + '={}', o)
            if r is not None:
                if self.is_timestr_valid(r[0]):
                    op_dict[const.PARAM_ATIME] = r[0]
                    continue
                else:
                    self.msg = const.ERRMSG \
                            + const.ERRMSG_DELIMITER \
                            + const.PARAM_ATIME \
                            + const.ERRMSG_DELIMITER \
                            + const.ERRMSG_INVALID_TIME
                    return {}

            r = parse.parse('--' + const.PARAM_LTIME + '={}', o)
            if r is not None:
                if self.is_timestr_valid(r[0]):
                    op_dict[const.PARAM_LTIME] = r[0]
                    continue
                else:
                    self.msg = const.ERRMSG \
                            + const.ERRMSG_DELIMITER \
                            + const.PARAM_LTIME \
                            + const.ERRMSG_DELIMITER \
                            + const.ERRMSG_INVALID_TIME
                    return {}

            r = parse.parse('--' + const.PARAM_COW + '={}', o)
            if r is not None:
                op_dict['cow'] = r[0]
                continue

            self.msg = const.ERRMSG
            return {}

        return op_dict

    def is_timestr_valid(self, timestr):
        ''' 時間が正しいかチェックする '''
        try:
            newDate = time.strptime(timestr,'%H:%M')
            return True
        except ValueError:
            return False

