import time

import basic_data_crawler
import gameid_info_crawler

if __name__ == '__main__':
    time_start = time.time()
    print('crawler started... good luck')
    # crawler = basic_data_crawler.TeamDataCrawler()
    # crawler.page_collector()
    # print(crawler.craw_basic_info())
    # crawler.craw_team_img()
    # print(crawler.craw_player_info())
    # crawler.close()
    crawler = gameid_info_crawler.GameIDInfoCrawler()
    crawler.page_collector()
    print('second %s: finish collecting pages' % (str(time.time() - time_start)))
    gameid_data, id_mapping = crawler.craw_gameid_info()
    print('second %s: finish parsing pages' % (str(time.time() - time_start)))
    print('length of data list:', len(gameid_data))
    print(gameid_data)
    print('length of id maping list:', len(id_mapping))
    print(id_mapping)
    crawler.close()
    print('end in %s seconds' % (str(time.time() - time_start)))
