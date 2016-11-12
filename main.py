import sys
import time

import basic_data_crawler
import dbhandler
import gameid_info_crawler
from models import Team, Player, IDMapping, GameIDInfo

if __name__ == '__main__':
    print('get argument:', sys.argv)
    time_start = time.time()
    db_handler = dbhandler.DBHandler()
    print('crawler started... good luck')
    if 'basic' in sys.argv:
        print('start to collect team and player pages')
        crawler = basic_data_crawler.TeamDataCrawler()
        crawler.page_collector()
        print('second %s: collecting pages finished' % (str(time.time() - time_start)))
        print('start to parse team data page')
        team_data = crawler.crawl_basic_info()
        print('second %s: crawling team data finished' % (str(time.time() - time_start)))
        print('team data:\n', team_data)
        print('start to save team data to db')
        db_handler.save_data(team_data, Team)
        print('crawling team img')
        crawler.crawl_team_img()
        print('start to parse player data page')
        player_data = crawler.crawl_player_info()
        print('second %s: crawling player data finished' % (str(time.time() - time_start)))
        print('play data:\n', player_data)
        print('start to save player data to db')
        db_handler.save_data(player_data, Player)
        crawler.close()
    if 'daily' in sys.argv and 'fix' not in sys.argv:
        crawler = gameid_info_crawler.GameIDInfoCrawler()
        crawler.page_collector()
        print('second %s: collecting pages finished' % (str(time.time() - time_start)))
        gameid_data, id_mapping = crawler.crawl_gameid_info()
        print('second %s: parsing pages finished' % (str(time.time() - time_start)))
        print('length of game id data list:', len(gameid_data))
        print('game id data:\n', gameid_data)
        print('start to save player data to db')
        db_handler.save_data(gameid_data, GameIDInfo)
        print('length of id maping list:', len(id_mapping))
        print('id mapping data:\n', id_mapping)
        print('start to save player data to db')
        db_handler.save_data(id_mapping, IDMapping)
        db_handler.update_summary()
        crawler.close()
    if 'daily' in sys.argv and 'fix' in sys.argv:
        crawler = gameid_info_crawler.GameIDInfoCrawler()
        crawler.fix_flag = 'yes'
        gameid_data, id_mapping = crawler.crawl_gameid_info()
        print('second %s: parsing pages finished' % (str(time.time() - time_start)))
        print('length of game id data list:', len(gameid_data))
        print('game id data:\n', gameid_data)
        print('start to save player data to db')
        db_handler.save_data(gameid_data, GameIDInfo)
        print('length of id maping list:', len(id_mapping))
        print('id mapping data:\n', id_mapping)
        print('start to save player data to db')
        db_handler.save_data(id_mapping, IDMapping)
        db_handler.update_idmapping_manual()
        db_handler.update_summary()
        crawler.close()
    if 'test' in sys.argv:
        # db_handler.update_idmapping_manual()
        # db_handler.update_summary()
        print(db_handler.get_idmappingmanual_gameid())
    if 'basic' not in sys.argv and 'daily' not in sys.argv and 'test' not in sys.argv:
        print('wrong argument')
    print('end in %s seconds' % (str(time.time() - time_start)))
