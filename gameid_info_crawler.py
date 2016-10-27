import time
from selenium import webdriver


class GameIDInfoCrawler(object):
    def __init__(self):
        self.browser = webdriver.PhantomJS(executable_path='/opt/phantomjs/bin/phantomjs')
        self.url = 'http://www.op.gg/ranking/ladder/'
        self.pages = []
        self.gameid_data = []

    def page_collector(self):
        self.browser.get(self.url)
        print('hello')
        js = "document.body.scrollTop=10000"
        count = 1
        while count < 100:
            self.browser.execute_script(js)
            time.sleep(1)
            count += 1
        page_ladder = self.browser.page_source
        print(len(page_ladder))
        all_player = self.browser.find_element_by_xpath('//tbody[@class="Body"]').find_elements_by_xpath('//tr[contains(@class,"Row")]')
        for player in all_player:
            if player.find_element_by_xpath('//td[contains(@class,"TierRank")]').text == 'Diamond 1':
                break
            print(player)
            player.find_element_by_xpath('//td[contains(@class,"SummonerName") and contains(@class,"Cell")]').click()
            time.sleep(2)
        for handle in self.browser.window_handles:
            self.browser.switch_to_window(handle)
            self.pages.append(self.browser.page_source)
        del (self.pages[0])
        print(len(self.pages))

    def craw_gameid_info(self):
        pass

    def close(self):
        self.browser.close()
        self.browser.quit()
