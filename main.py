import basic_data_crawler
import gameid_info_crawler

if __name__ == '__main__':
    print('start crawler...')
    # crawler = basic_data_crawler.TeamDataCrawler()
    # crawler.page_collector()
    # print(crawler.craw_basic_info())
    # crawler.craw_team_img()
    # print(crawler.craw_player_info())
    # crawler.close()
    crawler = gameid_info_crawler.GameIDInfoCrawler()
    crawler.page_collector()
    # print(crawler.craw_gameid_info())
    crawler.close()
    print('end')
