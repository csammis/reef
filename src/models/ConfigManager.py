""" Management for site configuration ORM objects """
from models import DBSession
from models.MeasurementType import MeasurementType
from models.Tank import Tank
from models.ScheduledEvent import ScheduledEvent
from models.InUseException import InUseException
from sqlalchemy.exc import IntegrityError

class ConfigManager(object):
    """ A manager for site configuration ORM objects """

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
        """ Delete an object from the database (can raise InUseException) """
        try:
            DBSession().delete(obj)
            DBSession().commit()
        except IntegrityError:
            DBSession().rollback()
            raise InUseException

    @staticmethod
    def get_measurement_type(measurement_type_id):
        """ Get a MeasurementType by ID """
        query = DBSession().query(MeasurementType).filter(MeasurementType.id == measurement_type_id)
        if query.count() == 0:
            return None
        return query.first()

    @staticmethod
    def get_measurement_types():
        """ Get a list of all MeasurementTypes """
        query = DBSession().query(MeasurementType)
        return query.order_by(MeasurementType.label.asc()).all()

    @staticmethod
    def update_measurement_type(measurement_type_id, label, units, acceptable_range):
        """ Update a MeasurementType """
        update_dict = {MeasurementType.label: label, MeasurementType.units: units}
        update_dict[MeasurementType.acceptable_range_low] = min(acceptable_range) if acceptable_range is not None else None
        update_dict[MeasurementType.acceptable_range_high] = max(acceptable_range) if acceptable_range is not None else None

        DBSession().query(MeasurementType).filter(MeasurementType.id == measurement_type_id).update(update_dict)
        DBSession().commit()

    @staticmethod
    def get_tank(tank_id):
        """ Get a Tank by ID """
        query = DBSession().query(Tank).filter(Tank.id == tank_id)
        if query.count() == 0:
            return None
        return query.first()

    @staticmethod
    def get_tank_from_name(tank_name):
        """ Get a Tank by name """
        query = DBSession().query(Tank).filter(Tank.name == tank_name)
        if query.count() == 0:
            return None
        return query.first()

    @staticmethod
    def get_tanks():
        """ Get a list of all Tanks """
        query = DBSession().query(Tank)
        return query.order_by(Tank.name.asc()).all()

    @staticmethod
    def update_tank(tank_id, name):
        """ Update a Tank """
        update_dict = {Tank.name: name}
        DBSession().query(Tank).filter(Tank.id == tank_id).update(update_dict)
        DBSession().commit()

    @staticmethod
    def get_scheduled_events(tank_id):
        """ Get a list of ScheduledEvents by tank ID """
        query = DBSession().query(ScheduledEvent).filter(ScheduledEvent.tank_id == tank_id)
        return query.order_by(ScheduledEvent.event_name.asc()).all()

    @staticmethod
    def get_scheduled_event(event_id):
        """ Get a ScheduledEvent by ID """
        query = DBSession().query(ScheduledEvent).filter(ScheduledEvent.id == event_id)
        if query.count() == 0:
            return None
        return query.first()

    @staticmethod
    def update_scheduled_event(event_id, update_dict):
        """ Update a ScheduledEvent """
        DBSession().query(ScheduledEvent).filter(ScheduledEvent.id == event_id).update(update_dict)
        DBSession().commit()
