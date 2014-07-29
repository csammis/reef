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
