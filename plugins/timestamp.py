from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import os
from urllib.parse import urlencode
from datetime import datetime
from abc import ABCMeta, abstractmethod

import const


class AbsCrawler:
    '''
    Strategyパターン
    クロール実行抽象クラス
    '''

    def __init__(self):
        self.user_info = None
        # ドライバを生成
        self.driver = self.init_driver()
        # 2秒待機
        self.wait = WebDriverWait(self.driver, 2)

    def set_user_info(self, user_info):
        ''' ユーザー情報のセッター '''
        self.user_info = user_info

    @abstractmethod
    def run(self):
        pass

    #######################################
    # ページ遷移
    #######################################

    def proc_with_page_move(self, func):
        ''' ページ読み込みを含む処理 '''
        # 関数実行
        func()
        # ページが読み込まれるまで待機
        self.wait.until(ec.presence_of_all_elements_located)

    def go_page(self, page_url):
        ''' 指定した画面に遷移 '''
        self.driver.get(page_url)

    def go_login_page(self):
        ''' ログイン画面に遷移 '''
        page_url = const.LOGIN_URL
        self.go_page(page_url)

    def go_time_stamp_page(self):
        ''' 打刻画面に遷移 '''
        page_url = const.TIME_STAMP_URL
        self.go_page(page_url)

    def go_shinsei_page(self):
        ''' 残業申請画面に遷移 '''

        # パラメータを設定
        params = self.user_info['shinsei_param']
        params['f_user_id']     = self.user_info['id']
        params['f_office_id']   = self.user_info['office_id']

        nowStr = datetime.now().strftime('%Y%m%d')
        params['f_shift_index'] = nowStr \
                                + self.user_info['start_hour'] \
                                + self.user_info['start_min'] + '00'
        params['f_kinmubi']     = nowStr
        page_url = self.constructUrl(const.SHINSEI_URLS, params)

        self.go_page(page_url)

    #######################################
    # フォーム送信
    #######################################

    def login(self):
        ''' ログインフォーム '''
        loginid = self.driver.find_element_by_id('id')
        password = self.driver.find_element_by_id('pass')

        loginid.send_keys(self.user_info['id'])
        password.send_keys(self.user_info['pw'])

        self.driver.find_element_by_name("form01").submit()

    def stamp_start(self):
        ''' 出勤打刻フォーム '''
        self.set_option(const.FORM_NAME_11, self.user_info['office_id'])
        self.set_option(const.FORM_NAME_16, self.user_info['department'])
        self.set_option(const.FORM_NAME_12, '1')

        self.driver.find_element_by_name("form01").submit()

    def stamp_finish(self):
        ''' 退勤打刻フォーム '''
        self.set_option(const.FORM_NAME_11, self.user_info['office_id'])
        self.set_option(const.FORM_NAME_16, self.user_info['department'])
        self.set_option(const.FORM_NAME_18, self.user_info['next_department'])
        self.set_option(const.FORM_NAME_12, '4')

        self.driver.find_element_by_name("form01").submit()

    def apply_overtime(self):
        ''' 残業申請処理の実行 '''
        pass

    #######################################
    # その他
    #######################################

    def init_driver(self):
        ''' ドライバのインスタンス生成 '''
        driver_path = const.DRIVER_PATH
        user_agent = const.USER_AGENT
        dcap = {
            "phantomjs.page.settings.userAgent" : user_agent,
            'marionette' : True
        }
        driver = webdriver.PhantomJS(
                executable_path=driver_path,
                desired_capabilities=dcap)

        return driver

    def set_option(self, sel, op):
        ''' プルダウンに値を設定する '''
        target_path = "//select[@name='" \
                        + sel \
                        + "']/option[@value='" \
                        + op + "']"
        self.driver.find_element_by_xpath(target_path).click()

    def take_screen_shot(self):
        ''' スクリーンショットを取る '''
        # Get Screen Shot
        FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screen.png")
        self.driver.save_screenshot(FILENAME)
        return FILENAME

    def constructUrl(self, url, params):
        ''' パラメータ付きのURLを生成する '''
        return url + '?' + urlencode(params)

class StartStampCrawler(AbsCrawler):
    ''' 出勤打刻クラス '''
    def __init__(self):
        super().__init__()

    def run(self):
        # ログインページ遷移
        super().proc_with_page_move(super().go_login_page)
        # ログイン実行
        super().proc_with_page_move(super().login)
        ## 打刻画面遷移
        super().proc_with_page_move(super().go_time_stamp_page)
        ## 出勤打刻実行
        super().proc_with_page_move(super().stamp_start)
        # スクショ
        img_path = super().take_screen_shot()
        # ドライバを閉じる
        self.driver.quit()
        # スクショのパスを返す
        return img_path

class FinishStampCrawler(AbsCrawler):
    ''' 退勤打刻クラス '''
    def __init__(self):
        super().__init__()

    def run(self):
        # ログインページ遷移
        super().proc_with_page_move(super().go_login_page)
        # ログイン実行
        super().proc_with_page_move(super().login)
        # 打刻画面遷移
        super().proc_with_page_move(super().go_time_stamp_page)
        # 退勤打刻実行
        super().proc_with_page_move(super().stamp_finish)
        # スクショ
        img_path = super().take_screen_shot()
        # ドライバを閉じる
        self.driver.quit()
        # スクショのパスを返す
        return img_path

class ApplyOvertimeCrawler(AbsCrawler):
    ''' 残業申請クラス '''
    def __init__(self):
        super().__init__()

    def run(self):
        # ログインページ遷移
        super().proc_with_page_move(super().go_login_page)
        # ログイン実行
        super().proc_with_page_move(super().login)
        # 申請画面遷移
        super().proc_with_page_move(super().go_shinsei_page)
        # 申請実行
        #super().proc_with_page_move(super().apply_overtime)
        # スクショ
        img_path = super().take_screen_shot()
        # ドライバを閉じる
        self.driver.quit()
        # スクショのパスを返す
        return img_path

class CrawlRunner():
    ''' Context Class '''
    def __init__(self, crawler):
        self.crawler = crawler

    def run(self, user_info):
        self.crawler.set_user_info(user_info)
        return self.crawler.run();
