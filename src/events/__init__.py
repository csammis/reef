from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

DBSession = scoped_session(sessionmaker())
Base = declarative_base()

def initialize_sql(dbname):
    engine = create_engine('sqlite:///' + dbname)
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)

from events.Measurement import Measurement
from events.LogEntry import LogEntry
from events.EventManager import EventManager
