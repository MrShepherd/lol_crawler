import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Summary


class DBHandler(object):
    def __init__(self):
        self.engine = create_engine('mysql+mysqlconnector://lolhfdev:lolhfdev@localhost:3306/lolhfdev')
        self.DBSession = sessionmaker(bind=self.engine)

    def initial_table(self, table_model):
        session = self.DBSession()
        session.query(table_model).delete()
        session.commit()
        session.close()

    def save_data(self, data_list, table_model):
        self.initial_table(table_model)
        for data in data_list:
            try:
                session = self.DBSession()
                row = table_model(**data)
                print('saving:', row)
                session.add(row)
                session.commit()
                session.close()
            except Exception as e:
                print(e)
                continue

    def update_summary(self):
        self.initial_table(Summary)
        time.sleep(10)
        session = self.DBSession()
        sql = '''
        insert into summary
        select
        COALESCE(c.player_name,'路人') as 'player_name'
        ,COALESCE(c.player_country,'unknown') as 'player_country'
        ,COALESCE(c.player_team_short_name,'路人') as 'player_team_short_name'
        ,COALESCE(c.player_team_league,'路人') as 'player_team_league'
        ,COALESCE(c.player_place,'路人') as 'player_place'
        ,a.*
        from gameidinfo a
        left join idmapping b
        on a.game_id=b.game_id
        left JOIN
        (
        SELECT * from player where player_name IN
        (
        SELECT player_name FROM player GROUP BY player_name HAVING count(*)=1
        )
        ) c
        on b.player_name=c.player_name
        ;
        '''
        print('update summary')
        session.execute(sql)
        session.commit()
        session.close()
