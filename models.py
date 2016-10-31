from sqlalchemy import Column, String, Integer, Float
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
    player_team_full_name = Column(String(50), primary_key=True)
    player_team_short_name = Column(String(50))
    player_team_country = Column(String(20))
    player_team_league = Column(String(20))
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
    rank = Column(Integer)
    tier = Column(String(30))
    lp = Column(Integer)
    total_win = Column(Integer)
    total_lose = Column(Integer)
    total_win_ratio = Column(Integer)
    mmr = Column(Integer)
    twentywin = Column(Integer)
    twentylose = Column(Integer)
    twentywinratio = Column(Integer)
    twentyavgkill = Column(Float)
    twentyavgdeath = Column(Float)
    twentyavgassist = Column(Float)
    twentyavgkda = Column(Float)
    twentyavgck = Column(Float)

    def __repr__(self):
        return '<GameIDInfo %r>' % self.game_id

