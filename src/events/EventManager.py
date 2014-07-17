from events import initialize_sql, DBSession
from events.Measurement import Measurement
from events.LogEntry import LogEntry
import datetime

class EventManager(object):

    def __init__(self, dbname):
        initialize_sql(dbname)

    def add(self, obj):
        DBSession.add(obj)
        DBSession.commit()
        return obj.id;

    def get_measurement(self, measurement_id):
        query = DBSession.query(Measurement).filter(Measurement.id == measurement_id)
        if query.count() == 0:
            return None
        return query.first()

    def get_log_entry(self, logentry_id):
        query = DBSession.query(LogEntry).filter(LogEntry.id == logentry_id)
        if query.count() == 0:
            return None
        return query.first()

    def get_measurements(self, parameters = None, timerange = {}):
        query = DBSession.query(Measurement)
        if parameters is not None:
            query = query.filter(Measurement.measurement_type.in_(parameters))
        if 'start' in timerange:
            query = query.filter(Measurement.measurement_time >= timerange['start'])
        if 'end' in timerange:
            query = query.filter(Measurement.measurement_time <= timerange['end'])
        return query.order_by(Measurement.measurement_time.asc()).all()

    def get_log_entries(self, timerange = {}):
        query = DBSession.query(LogEntry)
        if 'start' in timerange:
            query = query.filter(LogEntry.entry_time >= timerange['start'])
        if 'end' in timerange:
            query = query.filter(LogEntry.entry_time <= timerange['end'])
        return query.order_by(LogEntry.entry_time.asc()).all()

