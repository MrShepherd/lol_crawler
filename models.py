from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey

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
    player_team = Column(String(50))
    player_place = Column(String(20))

    def __repr__(self):
        return '<Player %r>' % self.player_name


class IDMapping(Base):
    __tablename__ = 'idmapping'
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_name = Column(String(100))
    game_id = Column(String(100))

    def __repr__(self):
        return '<IDMapping %r>' % self.gameid


class GameIDInfo(Base):
    __tablename__ = 'gameidinfo'
    game_id = Column(String(100), primary_key=True)
    rank = Column(String(10))
    tier = Column(String(32))
    lp = Column(Integer)
    win = Column(Integer)
    lose = Column(Integer)
    winratio = Column(Float)
    mmr = Column(Integer)
    twentywin = Column(Integer)
    twentylose = Column(Integer)
    twentywinratio = Column(Float)
    twentyavgkill = Column(Float)
    twentyavgdeath = Column(Float)
    twentyavgassist = Column(Float)
    twentyavgkda = Column(Float)

    def __repr__(self):
        return '<GameIDInfo %r>' % self.name
