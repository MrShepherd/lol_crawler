from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Team(Base):
    __tablename__ = 'team'
    team_name = Column(String(100), primary_key=True)
    team_nation = Column(String(10))
    team_league = Column(String(10))

    def __repr__(self):
        return '<Team %r>' % self.team_name


class Player(Base):
    __tablename__ = 'player'
    # id = Column(Integer, primary_key=True, autoincrement='ignore_fk')
    player_name = Column(String(100), primary_key=True)
    player_country = Column(String(20))
    player_team = Column(String(50), primary_key=True)
    player_place = Column(String(20))

    def __repr__(self):
        return '<Player %r>' % self.player_name


class IDMapping(Base):
    __tablename__ = 'idmapping'
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_team = Column(String(50))
    player_name = Column(String(100))
    game_id = Column(String(100))

    def __repr__(self):
        return '<IDMapping %r>' % self.game_id


class GameIDInfo(Base):
    __tablename__ = 'gameidinfo'
    game_id = Column(String(100), primary_key=True)
    link = Column(String(500))
    rank = Column(String(10))
    tier = Column(String(30))
    lp = Column(String(30))
    total_win = Column(String(30))
    total_lose = Column(String(30))
    total_win_ratio = Column(String(30))
    mmr = Column(String(30))
    twentywin = Column(String(30))
    twentylose = Column(String(30))
    twentywinratio = Column(String(30))
    twentyavgkill = Column(String(30))
    twentyavgdeath = Column(String(30))
    twentyavgassist = Column(String(30))
    twentyavgkda = Column(String(30))
    twentyavgck = Column(String(30))

    def __repr__(self):
        return '<GameIDInfo %r>' % self.game_id
