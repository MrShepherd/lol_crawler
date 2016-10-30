import os
import time
from urllib import request

from selenium import webdriver

import htmlparser


class TeamDataCrawler(object):
    def __init__(self):
        self.browser = webdriver.PhantomJS(executable_path="/opt/phantomjs/bin/phantomjs")
        self.url = 'http://www.wanplus.com/lol/ranking'
        self.pages = []
        self.teampages = []
        self.playerpages = []
        self.team_data = []
        self.player_data = []
        self.nation_set = set()
        self.img_path = 'img'

    def page_collector(self):
        self.browser.get(self.url)
        count = 1
        while True:
            self.pages.append(self.browser.page_source)
            count += 1
            team_links = self.browser.find_element_by_id('teamranking_left_team').find_elements_by_tag_name('li')
            for team_link in team_links:
                print('click team list:', team_link)
                team_link.click()
                time.sleep(4)
                self.teampages.append(self.browser.page_source)
                player_link = self.browser.find_element_by_id('teamranking_middle_team_detail').find_element_by_class_name('ranking_default_img')
                print('click team icon:', player_link)
                player_link.click()
                time.sleep(2)
            if count == 4:
                break
            page_link = self.browser.find_element_by_id("teamranking_team_page").find_element_by_link_text(str(count))
            print('click page down:', page_link)
            page_link.click()
            time.sleep(4)
        for handle in self.browser.window_handles:
            self.browser.switch_to_window(handle)
            self.playerpages.append(self.browser.page_source)
        del (self.playerpages[0])
        print('collected %d team' % len(self.pages))
        print('collected %d player' % len(self.playerpages))

    def crawl_basic_info(self):
        for page in self.pages:
            temp_dict = {}
            soup = htmlparser.HtmlParser(page).get_soup()
            all_li = soup.find('ul', {'id': 'teamranking_left_team', 'class': 'nation_tab'}).find_all('li')
            for li in all_li:
                temp_dict = {}
                temp_dict['team_name'] = li.find('div', class_='teamname').get_text()
                temp_dict['team_nation'] = li.find('i').get('class')[1]
                self.nation_set.add(temp_dict['team_nation'])
                if temp_dict['team_nation'] in ['CN']:
                    temp_dict['team_league'] = 'LPL'
                elif temp_dict['team_nation'] in ['KR']:
                    temp_dict['team_league'] = 'LCK'
                elif temp_dict['team_nation'] in ['TW', 'HK']:
                    temp_dict['team_league'] = 'LMS'
                elif temp_dict['team_nation'] in ['US']:
                    temp_dict['team_league'] = 'LCS-NA'
                elif temp_dict['team_nation'] in ['EU']:
                    temp_dict['team_league'] = 'LCS-EU'
                else:
                    temp_dict['team_league'] = 'ELSE'
                self.team_data.append(temp_dict)
        print(self.nation_set)
        return self.team_data

    def crawl_team_img(self):
        if not os.path.exists(self.img_path + '/nation'):
            os.makedirs(self.img_path + '/nation')
        if not os.path.exists(self.img_path + '/team'):
            os.makedirs(self.img_path + '/team')
        for img_str in self.nation_set:
            url = 'https://static.wanplus.com/data/common/country/' + img_str + '.png'
            print('saving nation img:', url)
            request.urlretrieve(url, self.img_path + '/nation/' + img_str + '.png')
        for page in self.teampages:
            soup = htmlparser.HtmlParser(page).get_soup()
            img_link = soup.find('div', {'id': 'teamranking_middle_team_detail'}).find('img').get('src')
            img_name = soup.find('div', {'id': 'teamranking_middle_team_detail'}).find('img').get('alt') + '.png'
            print('saving team img:', img_link)
            request.urlretrieve(img_link, self.img_path + '/team/' + img_name)
        return 'ok'

    def crawl_player_info(self):
        if not os.path.exists(self.img_path + '/player'):
            os.makedirs(self.img_path + '/player')
        # print(len(self.playerpages))
        for page in self.playerpages:
            tmp_dict = {}
            soup = htmlparser.HtmlParser(page).get_soup()
            # print('hello')
            if soup.find('ul', class_='tm_partner_list') is None or len(soup.find('ul', class_='tm_partner_list')) == 0:
                continue
            all_li = soup.find('ul', class_='tm_partner_list').find_all('li')
            for li in all_li:
                tmp_dict = {}
                tmp_dict['player_team'] = soup.find('table', class_='team_tba1').find('img').get('alt')
                tmp_dict['player_name'] = li.find('img').get('alt')
                img_name = tmp_dict['player_name'] + '.png'
                img_link = li.find('img').get('src')
                print('saving player img:', img_link)
                request.urlretrieve(img_link, self.img_path + '/player/' + img_name)
                tmp_dict['player_country'] = li.find('i').get('class')[1]
                tmp_dict['player_place'] = li.find('strong').get_text().split(':')[1]
                self.player_data.append(tmp_dict)
        return self.player_data

    def close(self):
        self.browser.close()
        self.browser.quit()
