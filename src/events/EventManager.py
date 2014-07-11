from events import initialize_sql, DBSession
from events.Measurement import Measurement
from events.LogEntry import LogEntry
import datetime

def pad_tuple(tpl, value, length):
    return tpl + (value,) * (length - len(tpl))

class EventManager(object):

    def __init__(self, dbname):
        initialize_sql(dbname)

    def add(self, obj):
        DBSession.add(obj)
        DBSession.commit()

    def get_measurements(self, parameters = None, timerange = None):
        query = DBSession.query(Measurement)
        if parameters is not None:
            query = query.filter(Measurement.measurement_type.in_(parameters))
        if timerange is not None:
            query = query.filter(Measurement.measurement_time.\
                    between(*pad_tuple(timerange, datetime.datetime.utcnow(), 2)))
        return query.order_by(Measurement.measurement_time.asc()).all()

    def get_log_entries(self, timerange = None):
        query = DBSession.query(LogEntry)
        if timerange is not None:
            query = query.filter(LogEntry.entry_time.\
                    between(*pad_tuple(timerange, datetime.datetime.utcnow(), 2)))
        return query.order_by(LogEntry.entry_time.asc()).all()

