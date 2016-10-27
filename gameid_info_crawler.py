import time
from urllib import parse, request

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import htmlparser


class GameIDInfoCrawler(object):
    def __init__(self):
        self.browser = webdriver.PhantomJS(executable_path='/opt/phantomjs/bin/phantomjs')
        # self.browser = webdriver.Chrome()
        self.browser.set_page_load_timeout(10)
        self.url = 'http://www.op.gg/ranking/ladder/'
        self.page_urls = []
        self.pages = []
        self.gameid_data = []
        self.img_path = 'img/gameid/'

    def page_collector(self):
        try:
            self.browser.get(self.url)
        except TimeoutException:
            self.browser.execute_script('window.stop()')
        print('hello')
        count = 1
        while count < 20:
            print(count)
            js = "document.body.scrollTop=%d000" % (count * 500)
            self.browser.execute_script(js)
            time.sleep(1)
            count += 1
        # page_ladder = self.browser.page_source
        # print(len(page_ladder))
        all_player = self.browser.find_element_by_xpath('//tbody[@class="Body"]').find_elements_by_xpath('//tr[contains(@class,"Row")]')
        print(len(all_player))
        for player in all_player[1:-1]:
            # if player.find_element_by_xpath('//td[contains(@class,"TierRank")]').text == 'Diamond 1':
            #     break
            # print(player.find_element_by_xpath('//td[contains(@class,"TierRank")]').text)
            if player.find_elements_by_tag_name('td')[3].text == 'Diamond 1':
                break
            # print(player)
            # print(player.text)
            # tmp_link = player.find_element_by_xpath('//td[contains(@class,"SummonerName")]/a').get_attribute('href')
            tmp_link = player.find_element_by_tag_name('a').get_attribute('href')
            tmp_full_link = parse.urljoin(self.url, tmp_link)
            print(tmp_full_link)
            self.page_urls.append(tmp_full_link)
        print(len(self.page_urls))

    def page_generator(self):
        for url in self.page_urls:
            print(url)
            try:
                self.browser.get(url)
            except TimeoutException:
                self.browser.execute_script('window.stop()')
            # time.sleep(2)
            self.browser.find_element_by_xpath('//div[@class="Buttons"]/button[contains(text(),"Check MMR")]').click()
            WebDriverWait(self.browser, 60).until(EC.presence_of_element_located((By.ID, 'ExtraView')))
            self.browser.find_element_by_xpath('//div[@class="RealContent"]//li[@data-type="ranked"]/a').click()
            WebDriverWait(self.browser, 60).until(EC.presence_of_element_located((By.ID, 'WinRatioSparkline')))
            print(len(self.browser.page_source))
            self.pages.append(self.browser.page_source)
        print(len(self.pages))

    def craw_gameid_info(self):
        count = 0
        for page in self.pages:
            soup = htmlparser.HtmlParser(page).get_soup()
            tmp_dict = {}
            tmp_dict['link'] = self.page_urls[count]
            count += 1
            tmp_dict['id'] = soup.find('div', class_='Profile').find('span', class_='Name').get_text()
            tmp_dict['rank'] = soup.find('div', class_='Rank').find('a').get_text()
            link = soup.find('div', class_='Face').find('img').get('src')
            print(link)
            request.urlretrieve(link, self.img_path + tmp_dict['id'] + '.png')
            tmp_dict['tier'] = soup.find('div', class_='TierRankInfo').find('span', class_='tierRank').get_text()
            tmp_dict['lp'] = soup.find('div', class_='TierRankInfo').find('span', class_='LeaguePoints').get_text().split(' ')[0].replace(',', '')
            tmp_dict['total_win'] = soup.find('div', class_='TierRankInfo').find('span', class_='wins').get_text().replace('W', '')
            tmp_dict['total_lose'] = soup.find('div', class_='TierRankInfo').find('span', class_='losses').get_text().replace('L', '')
            tmp_dict['total_win_ratio'] = soup.find('div', class_='TierRankInfo').find('span', class_='winratio').get_text().split(' ')[2]
            tmp_dict['mmr'] = soup.find('div', id='ExtraView').find('td', class_='MMR').get_text().replace(',', '')
            tmp_dict['20win'] = soup.find('div', class_='Box').find('div', class_='WinRatioTitle').get_text().split('')[1].replace('W', '')
            tmp_dict['20lose'] = soup.find('div', class_='Box').find('div', class_='WinRatioTitle').get_text().split('')[2].replace('L', '')
            tmp_dict['20winratio'] = soup.find('div', class_='Box').find('div', class_='WinRatioText').get_text()
            tmp_dict['20kill'] = soup.find('div', class_='KDA').find('span', class_='Kill').get_text()
            tmp_dict['20death'] = soup.find('div', class_='KDA').find('span', class_='Death').get_text()
            tmp_dict['20assist'] = soup.find('div', class_='KDA').find('span', class_='Assist').get_text()
            tmp_dict['20kda'] = soup.find('div', class_='KDARatio').find('span', class_='KDARatio').get_text().split(':')[0]
            tmp_dict['20kda'] = soup.find('div', class_='KDARatio').find('span', class_='CKRate').get_text().split(' ')[2].replace(')', '')

    def close(self):
        self.browser.close()
        self.browser.quit()
