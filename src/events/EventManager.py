from events import initialize_sql, DBSession
from events.Measurement import Measurement
from events.LogEntry import LogEntry
import datetime

class EventManager(object) :

    def __init__(self) :
        initialize_sql()

    def add(self, obj) :
        DBSession.add(obj)
        DBSession.commit()

    def get_measurements(self, timerange = None) :
        query = DBSession.query(Measurement)
        if timerange is not None :
            timerange += (datetime.datetime.now(),) * (2 - len(timerange))
            query = query.filter(Measurement.measurement_time.between(*timerange))
        return query.all()

    def get_log_entries(self, timerange = None) :
        query = DBSession.query(LogEntry)
        if timerange is not None :
            start, end = self.pad_with(timerange, datetime.datetime.now(), 2)
            query = query.filter(LogEntry.entry_time.between(start, end))
        return query.all()

    def pad_with(self, tpl, value, length) :
        return tpl + (value,) * (length - len(tpl))
