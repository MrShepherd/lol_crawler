from models import Team, Player, GameIDInfo, IDMapping
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBHandler(object):
    def __init__(self):
        self.engine = create_engine('mysql+mysqlconnector://lolhfdev:lolhfdev@localhost:3306/lolhfdev')
        self.DBSession = sessionmaker(bind=self.engine)

    def save_data(self, data_list, table_model):
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
