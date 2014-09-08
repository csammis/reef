from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

DBSession = scoped_session(sessionmaker())
Base = declarative_base()

def initialize_sql(dbname):
    engine = create_engine('sqlite:///' + dbname)
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)

@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON')
    cursor.close()

from models.InUseException import InUseException
from models.Measurement import Measurement
from models.LogEntry import LogEntry
from models.EventManager import EventManager
from models.MeasurementType import MeasurementType
from models.ConfigManager import ConfigManager
from models.Tank import Tank
from models.ScheduledEvent import ScheduledEvent

def has_minimum_setup():
    return True if DBSession.query(Tank).count() > 0 else False
