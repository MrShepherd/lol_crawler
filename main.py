import sys
import time

import basic_data_crawler
import dbhandler
from models import Team, Player

if __name__ == '__main__':
    arg = sys.argv[1]
    print('get argument:', arg)
    time_start = time.time()
    db_handler = dbhandler.DBHandler()
    print('crawler started... good luck')
    if arg == 'basic':
        print('start to collect team and player pages')
        crawler = basic_data_crawler.TeamDataCrawler()
        crawler.page_collector()
        print('second %s: collecting pages finished' % (str(time.time() - time_start)))
        print('start to parse team data page')
        team_data = crawler.crawl_basic_info()
        print('second %s: crawling team data finished' % (str(time.time() - time_start)))
        print('team data:\n', team_data)
        print('crawling team img')
        crawler.crawl_team_img()
        print('start to parse player data page')
        player_data = crawler.crawl_player_info()
        print('second %s: crawling player data finished' % (str(time.time() - time_start)))
        print('play data:\n', player_data)
        crawler.close()
        print('start to save team data to db')
        db_handler.save_data(team_data, Team)
        db_handler.save_data(player_data, Player)
    elif arg == 'daily':
        crawler = gameid_info_crawler.GameIDInfoCrawler()
        crawler.page_collector()
        print('second %s: collecting pages finished' % (str(time.time() - time_start)))
        gameid_data, id_mapping = crawler.crawl_gameid_info()
        print('second %s: parsing pages finished' % (str(time.time() - time_start)))
        print('length of data list:', len(gameid_data))
        print('game id data:\n', gameid_data)
        print('length of id maping list:', len(id_mapping))
        print('id mapping data:\n', id_mapping)
        crawler.close()
    else:
        print('wrong argument')
    print('end in %s seconds' % (str(time.time() - time_start)))
    db_handler.close()
