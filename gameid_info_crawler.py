import os
import random
import time
from multiprocessing.dummy import Pool
from urllib import parse, request

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import htmlparser


class GameIDInfoCrawler(object):
    def __init__(self):
        self.browser = webdriver.PhantomJS(executable_path='/opt/phantomjs/bin/phantomjs')
        # self.browser = webdriver.Chrome()
        self.browser.set_page_load_timeout(15)
        self.url = 'http://www.op.gg/ranking/ladder/'
        self.page_urls = []
        self.failed_downloaded_page_urls = []
        self.pages = []
        self.failed_parsed_pages = []
        self.gameid_data = []
        self.id_mapping = []
        self.img_path = 'img/gameid/'

    def page_generator(self, url):
        self.failed_downloaded_page_urls.remove(url)
        browser = webdriver.PhantomJS(executable_path='/opt/phantomjs/bin/phantomjs')
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
                self.failed_downloaded_page_urls.append(url)
                browser.close()
                browser.quit()
                return False
            except TimeoutException:
                self.failed_downloaded_page_urls.append(url)
                browser.close()
                browser.quit()
                return False
        except TimeoutException:
            self.failed_downloaded_page_urls.append(url)
            browser.close()
            browser.quit()
            return False
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
                self.failed_downloaded_page_urls.append(url)
                browser.close()
                browser.quit()
                return False
            except TimeoutException:
                self.failed_downloaded_page_urls.append(url)
                browser.close()
                browser.quit()
                return False
        except TimeoutException:
            self.failed_downloaded_page_urls.append(url)
            browser.close()
            browser.quit()
            return False
        print('length of html:', len(browser.page_source))
        page_source = browser.page_source
        self.pages.append(browser.page_source)
        print('number of pages succeffully downloaded:', len(self.pages))
        print('number of pages failed to download:', len(self.failed_downloaded_page_urls))
        browser.close()
        browser.quit()
        return page_source

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
                self.page_urls.append(tmp_full_link)
                # break
        print('length of url appended:', len(self.page_urls))
        self.failed_downloaded_page_urls = self.page_urls
        while len(self.failed_downloaded_page_urls) != 0:
            pool = Pool(8)
            pool.map(self.page_generator, self.failed_downloaded_page_urls)
            pool.close()
            pool.join()
        print('number of pages downloaded:', len(self.pages))

    def craw_gameid_info(self):
        base_url = 'http://www.op.gg/summoner/'
        # self.pages.append(request.urlopen('http://www.op.gg/summoner/userName=Jin%20Air%20Winged'))
        # self.pages.append(request.urlopen('http://www.op.gg/summoner/userName=%EA%B0%95%EC%B2%A0%EC%9D%98%EC%97%B0%EA%B8%88%EC%88%A04'))
        self.failed_parsed_pages = self.pages
        while len(self.failed_parsed_pages) != 0:
            print('number of pages failed to parse:', len(self.failed_parsed_pages))
            page = random.sample(self.failed_parsed_pages, 1)
            self.failed_parsed_pages.remove(page)
            tmp_dict = {}
            soup = htmlparser.HtmlParser(page).get_soup()
            try:
                tmp_dict['id'] = soup.find('div', class_='Profile').find_all('span', class_='Name')[-1].get_text()
                print('id:', tmp_dict['id'])
                tmp_dict['link'] = parse.urljoin(base_url, 'userName=' + tmp_dict['id'])
                print('link:', tmp_dict['link'])
                tmp_dict['rank'] = soup.find('div', class_='Rank').find('a').find('span').get_text()
                link = 'http:' + soup.find('div', class_='Face').find('img').get('src')
                print('img link:', link)
                if not os.path.exists(self.img_path):
                    os.makedirs(self.img_path)
                request.urlretrieve(link, self.img_path + tmp_dict['id'] + '.png')
                tmp_dict['tier'] = soup.find('div', class_='TierRankInfo').find('span', class_='tierRank').get_text()
                tmp_dict['lp'] = soup.find('div', class_='TierRankInfo').find('span', class_='LeaguePoints').get_text().split()[0].replace(',', '')
                tmp_dict['total_win'] = soup.find('div', class_='TierRankInfo').find('span', class_='wins').get_text().replace('W', '')
                tmp_dict['total_lose'] = soup.find('div', class_='TierRankInfo').find('span', class_='losses').get_text().replace('L', '')
                tmp_dict['total_win_ratio'] = soup.find('div', class_='TierRankInfo').find('span', class_='winratio').get_text().split()[2].replace('%', '')
                tmp_dict['mmr'] = soup.find('div', id='ExtraView').find('td', class_='MMR').get_text().replace(',', '').strip()
                tmp_dict['20win'] = soup.find('div', class_='GameAverageStats').find('div', class_='WinRatioTitle').get_text().split()[1].replace('W', '')
                tmp_dict['20lose'] = soup.find('div', class_='GameAverageStats').find('div', class_='WinRatioTitle').get_text().split()[2].replace('L', '')
                tmp_dict['20winratio'] = soup.find('div', class_='GameAverageStats').find('div', class_='WinRatioText').get_text().replace('%', '').replace('%', '')
                tmp_dict['20kill'] = soup.find('div', class_='GameAverageStats').find('span', class_='Kill').get_text()
                tmp_dict['20death'] = soup.find('div', class_='GameAverageStats').find('span', class_='Death').get_text()
                tmp_dict['20assist'] = soup.find('div', class_='GameAverageStats').find('span', class_='Assist').get_text()
                tmp_dict['20kda'] = soup.find('div', class_='KDARatio').find('span', class_='KDARatio').get_text().split(':')[0]
                tmp_dict['20CK'] = soup.find('div', class_='KDARatio').find('span', class_='CKRate').get_text().split()[2].replace(')', '').replace('%', '')
                self.gameid_data.append(tmp_dict)
                tmp_dict_2 = {}
                if soup.find('div', class_='Information').find('div', class_='Team') is not None:
                    tmp_dict_2['team'] = soup.find('div', class_='Information').find('div', class_='Team').get_text().strip().split('\n')[0]
                    tmp_dict_2['name'] = soup.find('div', class_='Information').find('span', class_='Name').get_text().replace('[', '').replace(']', '')
                    tmp_dict_2['id'] = tmp_dict['id']
                    self.id_mapping.append(tmp_dict_2)
            except Exception as e:
                print('failed:', tmp_dict['link'])
                print(e)
                self.failed_downloaded_page_urls.append((tmp_dict['link']))
                self.failed_parsed_pages.append(self.page_generator(tmp_dict['link']))
                continue

        return self.gameid_data, self.id_mapping

    def close(self):
        self.browser.close()
        self.browser.quit()
