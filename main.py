import basic_data_crawler

if __name__ == '__main__':
    print('start crawler...')
    crawler = basic_data_crawler.TeamDataCrawler()
    crawler.page_collector()
    print(crawler.craw_basic_info())
    crawler.craw_team_img()
    print(crawler.craw_player_info())
    crawler.close()
    print('end')
