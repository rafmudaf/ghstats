from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base


DeclarativeBase = declarative_base()


def db_connect(db_settings):
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    # for debug:
    # print("db_settings")
    # print(db_settings)
    url = db_settings["drivername"] + '://' + db_settings["username"] + ':' + db_settings["password"] + "@" + db_settings["host"] + ":" + db_settings["port"] + '/' + db_settings["database"]
    # for debug:
    # print("URL")
    # print(url)
    return create_engine(url, pool_timeout=60*60*24)


def create_tables(engine):
    """ Initialize all tables """
    DeclarativeBase.metadata.create_all(engine)


def recreate_all(engine):
    """ Delete all tables and data and recreate base tables """
    print("DROPPING AND RECREATING ALL TABLES")
    DeclarativeBase.metadata.drop_all(engine)
    DeclarativeBase.metadata.create_all(engine)


class Stats(DeclarativeBase):
    """Sqlalchemy stats data model"""
    __tablename__ = "stats"
    timestamp = Column('timestamp', DateTime, primary_key=True, unique=True)
    clones_total = Column('clones_total', Integer)
    clones_uniques = Column('clones_uniques', Integer)
    views_total = Column('views_total', Integer)
    views_uniques = Column('views_uniques', Integer)

class StatsNRELFloris(DeclarativeBase):
    """Sqlalchemy stats data model"""
    __tablename__ = "statsnrelfloris"
    timestamp = Column('timestamp', DateTime, primary_key=True, unique=True)
    clones_total = Column('clones_total', Integer)
    clones_uniques = Column('clones_uniques', Integer)
    views_total = Column('views_total', Integer)
    views_uniques = Column('views_uniques', Integer)

class StatswfcTools(DeclarativeBase):
    """Sqlalchemy stats data model"""
    __tablename__ = "statswfctools"
    timestamp = Column('timestamp', DateTime, primary_key=True, unique=True)
    clones_total = Column('clones_total', Integer)
    clones_uniques = Column('clones_uniques', Integer)
    views_total = Column('views_total', Integer)
    views_uniques = Column('views_uniques', Integer)