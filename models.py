from sqlalchemy import Column, String, Integer, Float, create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import ForeignKey

Base = declarative_base()


class Team(Base):
    __tablename__ = 'team'
    team_name = Column(String(100), primary_key=True)
    team_nation = Column(String(10))
    team_league = Column(String(10))
    players = relationship('Player', backref='team', lazy='dynamic')

    def __repr__(self):
        return '<Team %r>' % self.name


class Player(Base):
    __tablename__ = 'player'
    # id = Column(Integer, primary_key=True, autoincrement='ignore_fk')
    name = Column(String(64), primary_key=True)
    country = Column(String(32))
    team = Column(String(32), ForeignKey('team.name'))
    place = Column(String(16))
    idmappings = relationship('IDMapping', backref='player', lazy='dynamic')

    def __repr__(self):
        return '<Player %r>' % self.name


class IDMapping(Base):
    __tablename__ = 'idmapping'
    id = Column(Integer, primary_key=True, autoincrement=True)
    playername = Column(String(64), ForeignKey('player.name'), )
    gameid = Column(String(64))

    def __repr__(self):
        return '<IDMapping %r>' % self.name


class GameIDInfo(Base):
    __tablename__ = 'gameidinfo'
    gameid = Column(String(64), primary_key=True)
    rank = Column(Integer)
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
