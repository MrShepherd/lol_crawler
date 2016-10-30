from models import Team, Player
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBHandler(object):
    def __init__(self):
        self.engine = create_engine('mysql+mysqlconnector://lolhfdev:lolhfdev@localhost:3306/lolhfdev')
        self.DBSession = sessionmaker(bind=self.engine)
        self.session = self.DBSession()

    def save_data(self, data_list, table_model):
        for data in data_list:
            try:
                row = table_model(**data)
                print('saving:', row)
                self.session.add(row)
                self.session.commit()
            except Exception as e:
                print(e)
                continue

    def close(self):
        self.session.close()
