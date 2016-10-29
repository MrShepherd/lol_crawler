import models


class DBHandler(object):
    def __init__(self):
        self.engine = create_engine('mysql+mysqlconnector://lolhfdev:lolhfdev@localhost:3306/lolhfdev')
        self.DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def save_team_data(self, data_list):
        for data in data_list:
            team = Team(**data)
            self.session.add(team)

    def close(self):
        self.session.close()
