import os
from multiprocessing.dummy import Pool
from urllib import parse, request

import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import htmlparser


class GameIDInfoCrawler(object):
    def __init__(self):
        self.service_args = ['--proxy=122.96.59.107:843', '--proxy-type=http']
        self.browser = webdriver.PhantomJS(executable_path='/opt/phantomjs/bin/phantomjs', service_args=self.service_args)
        # self.browser = webdriver.Chrome()
        self.browser.set_page_load_timeout(15)
        self.url = 'http://www.op.gg/ranking/ladder/'
        self.pro_url = 'http://www.op.gg/spectate/list/'
        self.page_urls = set()
        self.failed_downloaded_page_urls = set()
        self.pages = []
        self.failed_parsed_pages = []
        self.gameid_data = []
        self.id_mapping = set()
        self.img_path = 'img/gameid/'

    def page_generator(self, url):
        self.failed_downloaded_page_urls.remove(url)
        service_args = ['--proxy=122.96.59.107:843', '--proxy-type=http']
        browser = webdriver.PhantomJS(executable_path='/opt/phantomjs/bin/phantomjs', service_args=service_args)
        # browser = webdriver.Chrome()
        browser.set_page_load_timeout(15)
        print('getting:', url)
        # get url
        try:
            browser.get(url)
        except TimeoutException:
            browser.execute_script('window.stop()')
        # click button
        try:
            browser.find_element_by_xpath('//div[@class="Buttons"]/button[contains(text(),"Check MMR")]').click()
            WebDriverWait(browser, 120).until(EC.presence_of_element_located((By.ID, 'ExtraView')))
        except NoSuchElementException:
            try:
                try:
                    browser.get(url)
                except TimeoutException:
                    browser.execute_script('window.stop()')
                browser.find_element_by_xpath('//div[@class="Buttons"]/button[contains(text(),"Check MMR")]').click()
                WebDriverWait(browser, 120).until(EC.presence_of_element_located((By.ID, 'ExtraView')))
            except NoSuchElementException:
                self.failed_downloaded_page_urls.add(url)
                browser.close()
                browser.quit()
                return url + '+' + ''
            except TimeoutException:
                self.failed_downloaded_page_urls.add(url)
                browser.close()
                browser.quit()
                return url + '+' + ''
        except TimeoutException:
            self.failed_downloaded_page_urls.add(url)
            browser.close()
            browser.quit()
            return url + '+' + ''
        # click link
        try:
            browser.find_element_by_xpath('//div[@class="RealContent"]//li[@data-type="ranked"]/a').click()
            WebDriverWait(browser, 120).until(EC.presence_of_element_located((By.ID, 'WinRatioSparkline')))
        except NoSuchElementException:
            try:
                try:
                    browser.get(url)
                except TimeoutException:
                    browser.execute_script('window.stop()')
                browser.find_element_by_xpath('//div[@class="RealContent"]//li[@data-type="ranked"]/a').click()
                WebDriverWait(browser, 120).until(EC.presence_of_element_located((By.ID, 'WinRatioSparkline')))
            except NoSuchElementException:
                self.failed_downloaded_page_urls.add(url)
                browser.close()
                browser.quit()
                return url + '+' + ''
            except TimeoutException:
                self.failed_downloaded_page_urls.add(url)
                browser.close()
                browser.quit()
                return url + '+' + ''
        except TimeoutException:
            self.failed_downloaded_page_urls.add(url)
            browser.close()
            browser.quit()
            return url + '+' + ''
        print('length of html:', len(browser.page_source))
        page_source = browser.page_source
        self.pages.append(url + '+' + browser.page_source)
        print('number of pages succeffully downloaded:', len(self.pages))
        print('number of pages failed to download:', len(self.failed_downloaded_page_urls))
        browser.close()
        browser.quit()
        return url + '+' + page_source

    def page_collector(self):
        try:
            self.browser.get(self.url)
        except TimeoutException:
            self.browser.execute_script('window.stop()')
        print('get %s successfully' % self.url)
        count = 1
        while count < 20:
            print(count, end='===>')
            time.sleep(2)
            js = "document.body.scrollTop=%d000" % (count * 500)
            self.browser.execute_script(js)
            count += 1
        all_player = self.browser.find_element_by_xpath('//tbody[@class="Body"]').find_elements_by_xpath('//tr[contains(@class,"Row")]')
        print('number of player found:', len(all_player))
        for player in all_player[1:-1]:
            if player.find_elements_by_tag_name('td')[3].text in ['Challenger', 'Master']:
                tmp_link = player.find_element_by_tag_name('a').get_attribute('href')
                tmp_full_link = parse.urljoin(self.url, tmp_link)
                print('append:', tmp_full_link)
                self.page_urls.add(tmp_full_link)
        try:
            self.browser.get(self.pro_url)
        except TimeoutException:
            self.browser.execute_script('window.stop()')
        print('get %s successfully' % self.pro_url)
        all_pro_link = self.browser.find_element_by_xpath('//ul[@class="RegisterSummonerList"]').find_elements_by_tag_name('a')
        for item in all_pro_link:
            tmp_link = item.get_attribute('href')
            tmp_full_link = parse.urljoin(self.url, tmp_link)
            print('append:', tmp_full_link)
            self.page_urls.add(tmp_full_link)
        print('length of url appended:', len(self.page_urls))
        self.failed_downloaded_page_urls = self.page_urls
        while len(self.failed_downloaded_page_urls) != 0:
            pool = Pool(8)
            pool.map(self.page_generator, self.failed_downloaded_page_urls)
            pool.close()
            pool.join()
        print('number of pages downloaded:', len(self.pages))

    def parse_gameid_info(self, page):
        base_url = 'http://www.op.gg/summoner/'
        print('number of pages failed to parse:', len(self.failed_parsed_pages))
        self.failed_parsed_pages.remove(page)
        tmp_dict = {}
        url = page.split('+', 1)[0]
        soup = htmlparser.HtmlParser(page.split('+', 1)[1]).get_soup()
        try:
            tmp_dict['game_id'] = soup.find('div', class_='Profile').find_all('span', class_='Name')[-1].get_text()
            print('game_id:', tmp_dict['game_id'])
            tmp_dict['link'] = parse.urljoin(base_url, 'userName=' + tmp_dict['game_id'])
            print('link:', tmp_dict['link'])
            tmp_dict['rank'] = soup.find('div', class_='Rank').find('a').find('span').get_text()
            link = 'http:' + soup.find('div', class_='Face').find('img').get('src')
            print('img link:', link)
            if not os.path.exists(self.img_path):
                os.makedirs(self.img_path)
            request.urlretrieve(link, self.img_path + tmp_dict['game_id'] + '.png')
            tmp_dict['tier'] = soup.find('div', class_='TierRankInfo').find('span', class_='tierRank').get_text()
            tmp_dict['lp'] = soup.find('div', class_='TierRankInfo').find('span', class_='LeaguePoints').get_text().split()[0].replace(',', '')
            tmp_dict['total_win'] = soup.find('div', class_='TierRankInfo').find('span', class_='wins').get_text().replace('W', '')
            tmp_dict['total_lose'] = soup.find('div', class_='TierRankInfo').find('span', class_='losses').get_text().replace('L', '')
            tmp_dict['total_win_ratio'] = soup.find('div', class_='TierRankInfo').find('span', class_='winratio').get_text().split()[2].replace('%', '')
            tmp_dict['mmr'] = soup.find('div', id='ExtraView').find('td', class_='MMR').get_text().replace(',', '').strip()
            tmp_dict['twentywin'] = soup.find('div', class_='GameAverageStats').find('div', class_='WinRatioTitle').get_text().split()[1].replace('W', '')
            tmp_dict['twentylose'] = soup.find('div', class_='GameAverageStats').find('div', class_='WinRatioTitle').get_text().split()[2].replace('L', '')
            tmp_dict['twentywinratio'] = soup.find('div', class_='GameAverageStats').find('div', class_='WinRatioText').get_text().replace('%', '').replace('%', '')
            tmp_dict['twentyavgkill'] = soup.find('div', class_='GameAverageStats').find('span', class_='Kill').get_text()
            tmp_dict['twentyavgdeath'] = soup.find('div', class_='GameAverageStats').find('span', class_='Death').get_text()
            tmp_dict['twentyavgassist'] = soup.find('div', class_='GameAverageStats').find('span', class_='Assist').get_text()
            tmp_dict['twentyavgkda'] = soup.find('div', class_='KDARatio').find('span', class_='KDARatio').get_text().split(':')[0]
            tmp_dict['twentyavgck'] = soup.find('div', class_='KDARatio').find('span', class_='CKRate').get_text().split()[2].replace(')', '').replace('%', '')
            self.gameid_data.append(tmp_dict)
            tmp_dict_2 = {}
            if soup.find('div', class_='Information').find('div', class_='Team') is not None:
                tmp_dict_2['player_team'] = soup.find('div', class_='Information').find('div', class_='Team').get_text().strip().split('\n')[0]
                tmp_dict_2['player_name'] = soup.find('div', class_='Information').find('span', class_='Name').get_text().replace('[', '').replace(']', '').upper()
                tmp_dict_2['game_id'] = tmp_dict['game_id']
                self.id_mapping.add(tmp_dict_2)
        except Exception as e:
            print('failed:', url)
            print(e)
            if soup.find('div', class_='SummonerNotFoundLayout') is not None:
                return
            self.failed_downloaded_page_urls.add(url)
            self.failed_parsed_pages.append(self.page_generator(url))

    def crawl_gameid_info(self):
        self.failed_parsed_pages = self.pages
        self.pages = []
        while len(self.failed_parsed_pages) != 0:
            pool = Pool(8)
            pool.map(self.parse_gameid_info, self.failed_parsed_pages)
            pool.close()
            pool.join()
        return self.gameid_data, self.id_mapping

    def close(self):
        self.browser.close()
        self.browser.quit()
