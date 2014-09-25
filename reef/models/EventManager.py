""" Management for per-tank event ORM objects """
from models import DBSession
from models.Measurement import Measurement
from models.MeasurementType import MeasurementType
from models.LogEntry import LogEntry
from sqlalchemy import func

class EventManager(object):
    """ A manager for per-tank event ORM objects """

    def __init__(self):
        pass

    @staticmethod
    def add(obj):
        """ Add a new object to the database """
        DBSession().add(obj)
        DBSession().commit()
        return obj.id

    @staticmethod
    def delete(obj):
        """ Delete an object from the database """
        DBSession().delete(obj)
        DBSession().commit()

    @staticmethod
    def get_measurement(measurement_id):
        """ Get a Measurement by ID """
        query = DBSession().query(Measurement).filter(Measurement.id == measurement_id)
        if query.count() == 0:
            return None
        return query.first()

    @staticmethod
    def get_log_entry(logentry_id):
        """ Get a LogEntry by ID """
        query = DBSession().query(LogEntry).filter(LogEntry.id == logentry_id)
        if query.count() == 0:
            return None
        return query.first()

    @staticmethod
    def get_measurements(tank_id=None, parameters=None, timerange=None):
        """ Get a list of Measurements """
        query = DBSession().query(Measurement)
        if tank_id is not None:
            query = query.filter(Measurement.tank_id == tank_id)
        if parameters is not None:
            query = query.filter(Measurement.measurement_type_id.in_(parameters))
        if timerange is not None:
            if 'start' in timerange:
                query = query.filter(Measurement.measurement_time >= timerange['start'])
            if 'end' in timerange:
                query = query.filter(Measurement.measurement_time <= timerange['end'])
        return query.order_by(Measurement.measurement_time.asc()).all()

    @staticmethod
    def get_latest_measurements(tank_id, as_of):
        """ Get a list of Measurements for a tank as of a specified date """
        query = (DBSession().query(func.max(Measurement.measurement_time), MeasurementType.label,
                                   Measurement.value, MeasurementType.units)
                 .join(MeasurementType)
                 .filter(Measurement.tank_id == tank_id)
                 .filter(Measurement.measurement_time <= as_of)
                 .group_by(MeasurementType.label)
                 .order_by(MeasurementType.label.asc()))
        return query.all()

    @staticmethod
    def get_log_entries(tank_id=None, timerange=None):
        """ Get a list of LogEntry objects """
        query = DBSession().query(LogEntry)
        if tank_id is not None:
            query = query.filter(LogEntry.tank_id == tank_id)
        if timerange is not None:
            if 'start' in timerange:
                query = query.filter(LogEntry.entry_time >= timerange['start'])
            if 'end' in timerange:
                query = query.filter(LogEntry.entry_time <= timerange['end'])
        return query.order_by(LogEntry.entry_time.asc()).all()

    @staticmethod
    def update_log_entry(logentry_id, entry, entry_time):
        """ Update a LogEntry """
        update_dict = {LogEntry.entry: entry, LogEntry.entry_time: entry_time}
        DBSession().query(LogEntry).filter(LogEntry.id == logentry_id).update(update_dict)
        DBSession().commit()
