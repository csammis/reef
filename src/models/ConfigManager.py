from models import DBSession
from models.MeasurementType import MeasurementType

class ConfigManager(object):

    def __init__(self):
        pass

    def add(self, obj):
        DBSession.add(obj)
        DBSession.commit()
        return obj.id

    def delete(self, obj):
        DBSession.delete(obj)
        DBSession.commit()

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
