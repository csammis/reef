from models import DBSession
from models.Measurement import Measurement
from models.MeasurementType import MeasurementType
from models.LogEntry import LogEntry
from sqlalchemy import func
import datetime

class EventManager(object):

    def __init__(self):
        pass

    def add(self, obj):
        DBSession.add(obj)
        DBSession.commit()
        return obj.id;

    def delete(self, obj):
        DBSession.delete(obj);
        DBSession.commit();

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

    def get_measurements(self, tank_id = None, parameters = None, timerange = {}):
        query = DBSession.query(Measurement)
        if tank_id is not None:
            query = query.filter(Measurement.tank_id == tank_id)
        if parameters is not None:
            query = query.filter(Measurement.measurement_type_id.in_(parameters))
        if 'start' in timerange:
            query = query.filter(Measurement.measurement_time >= timerange['start'])
        if 'end' in timerange:
            query = query.filter(Measurement.measurement_time <= timerange['end'])
        return query.order_by(Measurement.measurement_time.asc()).all()

    def get_latest_measurements(self, tank_id):
        query = DBSession.query(func.max(Measurement.measurement_time), MeasurementType.label, Measurement.value, MeasurementType.units)\
                .join(MeasurementType)\
                .filter(Measurement.tank_id == tank_id)\
                .group_by(MeasurementType.label)\
                .order_by(MeasurementType.label.asc())
        return query.all()

    def get_log_entries(self, tank_id = None, timerange = {}):
        query = DBSession.query(LogEntry)
        if tank_id is not None:
            query = query.filter(LogEntry.tank_id == tank_id)
        if 'start' in timerange:
            query = query.filter(LogEntry.entry_time >= timerange['start'])
        if 'end' in timerange:
            query = query.filter(LogEntry.entry_time <= timerange['end'])
        return query.order_by(LogEntry.entry_time.asc()).all()

    def update_log_entry(self, logentry_id, entry, entry_time):
        DBSession.query(LogEntry).filter(LogEntry.id == logentry_id).update({LogEntry.entry: entry, LogEntry.entry_time: entry_time})
        DBSession.commit()
