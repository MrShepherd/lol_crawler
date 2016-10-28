import random
import time
from urllib import parse, request

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from multiprocessing.dummy import Pool

import htmlparser


class GameIDInfoCrawler(object):
    def __init__(self):
        self.browser = webdriver.PhantomJS(executable_path='/opt/phantomjs/bin/phantomjs')
        # self.browser = webdriver.Chrome()
        self.browser.set_page_load_timeout(15)
        self.url = 'http://www.op.gg/ranking/ladder/'
        self.page_urls = []
        self.failed_page_urls = []
        self.pages = []
        self.gameid_data = []
        self.img_path = 'img/gameid/'

    def page_generator(self, url):
        browser = webdriver.PhantomJS(executable_path='/opt/phantomjs/bin/phantomjs')
        # browser = webdriver.Chrome()
        browser.set_page_load_timeout(15)
        print('getting:', url)
        self.failed_page_urls.remove(url)
        # get url
        try:
            browser.get(url)
        except TimeoutException:
            browser.execute_script('window.stop()')
        # click button
        try:
            browser.find_element_by_xpath('//div[@class="Buttons"]/button[contains(text(),"Check MMR")]').click()
            WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.ID, 'ExtraView')))
        except NoSuchElementException:
            try:
                browser.find_element_by_xpath('//div[@class="Buttons"]/button[contains(text(),"Check MMR")]').click()
                WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.ID, 'ExtraView')))
            except NoSuchElementException:
                self.failed_page_urls.append(url)
                browser.close()
                browser.quit()
                return False
        except TimeoutException:
            self.failed_page_urls.append(url)
            browser.close()
            browser.quit()
            return False
        # click link
        try:
            browser.find_element_by_xpath('//div[@class="RealContent"]//li[@data-type="ranked"]/a').click()
            WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.ID, 'WinRatioSparkline')))
        except NoSuchElementException:
            try:
                browser.find_element_by_xpath('//div[@class="RealContent"]//li[@data-type="ranked"]/a').click()
                WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.ID, 'WinRatioSparkline')))
            except NoSuchElementException:
                self.failed_page_urls.append(url)
                browser.close()
                browser.quit()
                return False
        except TimeoutException:
            self.failed_page_urls.append(url)
            browser.close()
            browser.quit()
            return False
        print('length of html:', len(browser.page_source))
        self.pages.append(browser.page_source)
        print('number of pages succeffully downloaded:', len(self.pages))
        print('number of pages failed to download:', len(self.failed_page_urls))
        browser.close()
        browser.quit()
        return True

    def page_collector(self):
        try:
            self.browser.get(self.url)
        except TimeoutException:
            self.browser.execute_script('window.stop()')
        print('get %s successfully' % self.url)
        count = 1
        while count < 16:
            print(count, end='===>')
            js = "document.body.scrollTop=%d000" % (count * 500)
            self.browser.execute_script(js)
            time.sleep(2)
            count += 1
        time.sleep(10)
        # page_ladder = self.browser.page_source
        # print(len(page_ladder))
        all_player = self.browser.find_element_by_xpath('//tbody[@class="Body"]').find_elements_by_xpath('//tr[contains(@class,"Row")]')
        print('number of player found:', len(all_player))
        for player in all_player[1:-1]:
            if player.find_elements_by_tag_name('td')[3].text == 'Diamond 1':
                break
            if player.find_elements_by_tag_name('td')[3].text in ['Challenger', 'Master']:
                tmp_link = player.find_element_by_tag_name('a').get_attribute('href')
                tmp_full_link = parse.urljoin(self.url, tmp_link)
                print('append:', tmp_full_link)
                self.page_urls.append(tmp_full_link)
        print('length of url appended:', len(self.page_urls))
        self.failed_page_urls = self.page_urls
        while len(self.failed_page_urls) != 0:
            pool = Pool(8)
            pool.map(self.page_generator, self.failed_page_urls)
            pool.close()
            pool.join()

    def craw_gameid_info(self):
        base_url = 'http://www.op.gg/summoner/'
        for page in self.pages:
            soup = htmlparser.HtmlParser(page).get_soup()
            tmp_dict = {}
            tmp_dict['id'] = soup.find('div', class_='Profile').find('span', class_='Name').get_text()
            tmp_dict['link'] = parse.urljoin(base_url, 'userName=' + tmp_dict['id'])
            tmp_dict['rank'] = soup.find('div', class_='Rank').find('a').get_text()
            link = soup.find('div', class_='Face').find('img').get('src')
            print('img link:', link)
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
            self.gameid_data.append(tmp_dict)

    def close(self):
        self.browser.close()
        self.browser.quit()
