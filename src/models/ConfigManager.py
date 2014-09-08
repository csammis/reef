from models import DBSession
from models.MeasurementType import MeasurementType
from models.Tank import Tank
from models.ScheduledEvent import ScheduledEvent
from models.InUseException import InUseException
from sqlalchemy.exc import IntegrityError

class ConfigManager(object):

    def __init__(self):
        pass

    def add(self, obj):
        DBSession.add(obj)
        DBSession.commit()
        return obj.id

    def delete(self, obj):
        try:
            DBSession.delete(obj)
            DBSession.commit()
        except IntegrityError:
            DBSession.rollback()
            raise InUseException

    def get_measurement_type(self, measurement_type_id):
        query = DBSession.query(MeasurementType).filter(MeasurementType.id == measurement_type_id)
        if query.count() == 0:
            return None
        return query.first()

    def get_measurement_types(self):
        query = DBSession.query(MeasurementType)
        return query.order_by(MeasurementType.label.asc()).all()

    def update_measurement_type(self, measurement_type_id, label, units, acceptable_range):
        updateDict = {MeasurementType.label: label, MeasurementType.units: units}
        updateDict[MeasurementType.acceptable_range_low] = min(acceptable_range) if acceptable_range is not None else None
        updateDict[MeasurementType.acceptable_range_high] = max(acceptable_range) if acceptable_range is not None else None

        DBSession.query(MeasurementType).filter(MeasurementType.id == measurement_type_id).update(updateDict)
        DBSession.commit()

    def get_tank(self, tank_id):
        query = DBSession.query(Tank).filter(Tank.id == tank_id)
        if query.count() == 0:
            return None
        return query.first()

    def get_tank_from_name(self, tank_name):
        query = DBSession.query(Tank).filter(Tank.name == tank_name)
        if query.count() == 0:
            return None
        return query.first()

    def get_tanks(self):
        query = DBSession.query(Tank)
        return query.order_by(Tank.name.asc()).all()

    def update_tank(self, tank_id, name):
        updateDict = {Tank.name: name}
        DBSession.query(Tank).filter(Tank.id == tank_id).update(updateDict)
        DBSession.commit()

    def get_scheduled_events(self, tank_id):
        query = DBSession.query(ScheduledEvent).filter(ScheduledEvent.tank_id == tank_id)
        return query.order_by(ScheduledEvent.event_name.asc()).all()
