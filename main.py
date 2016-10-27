import time

import basic_data_crawler
import gameid_info_crawler

if __name__ == '__main__':
    time_start = time.time()
    print('start crawler...')
    # crawler = basic_data_crawler.TeamDataCrawler()
    # crawler.page_collector()
    # print(crawler.craw_basic_info())
    # crawler.craw_team_img()
    # print(crawler.craw_player_info())
    # crawler.close()
    crawler = gameid_info_crawler.GameIDInfoCrawler()
    crawler.page_collector()
    crawler.page_generator()
    # print(crawler.craw_gameid_info())
    crawler.close()
    time_end = time.time()
    print('end in %s seconds') % (str(time_end - time_start))
