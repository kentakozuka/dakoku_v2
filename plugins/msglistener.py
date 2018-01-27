from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import default_reply

from msghandler import MessageHandler
from cmdhandler import CommandHandler
import timestamp as Ts
import const

@listen_to('おは')
def start_work(message):
    ''' 出勤打刻をする '''
    mh = MessageHandler( \
            message, \
            Ts.CrawlRunner(Ts.StartStampCrawler()), \
            const.msg_start_stamp, \
            const.msg_start_greeting)
    mh.run_crawler()

@listen_to('おつ')
def finish_work(message):
    ''' 退勤打刻をする '''
    mh = MessageHandler( \
            message, \
            Ts.CrawlRunner(Ts.FinishStampCrawler()), \
            const.msg_finish_stamp, \
            const.msg_finish_greeting)
    mh.run_crawler()

@listen_to('した')
def finish_work(message):
    ''' 残業申請をする '''
    mh = MessageHandler( \
            message, \
            Ts.CrawlRunner(Ts.ApplyOvertimeCrawler()), \
            const.msg_apply_overtime, \
            const.msg_apply_greeting)
    mh.run_crawler()

@respond_to('')
def mention_func(message):
    ''' すべてのダイレクトメッセージを待ち受ける '''
    ch = CommandHandler(message)
    message.reply(ch.get_msg())
