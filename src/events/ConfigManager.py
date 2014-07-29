from events import DBSession
from events.MeasurementConfig import MeasurementConfig

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
        query = DBSession.query(MeasurementConfig).filter(MeasurementConfig.id == measurement_type_id)
        if query.count() == 0:
            return None
        return query.first()

    def get_measurement_types(self):
        query = DBSession.query(MeasurementConfig)
        return query.order_by(MeasurementConfig.label.asc()).all()

    def update_measurement_type(self, measurement_type_id, label, units, acceptable_range):
        updateDict = {MeasurementConfig.label: label, MeasurementConfig.units: units}
        updateDict[MeasurementConfig.acceptable_range_low] = min(acceptable_range) if acceptable_range is not None else None
        updateDict[MeasurementConfig.acceptable_range_high] = max(acceptable_range) if acceptable_range is not None else None

        DBSession.query(MeasurementConfig).filter(MeasurementConfig.id == measurement_type_id).update(updateDict)
