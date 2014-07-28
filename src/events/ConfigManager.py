from events import DBSession
from events.MeasurementConfig import MeasurementConfig

class ConfigManager(object):

    def __init__(self):
        pass

    def add(self, obj):
        DBSession.add(obj)
        DBSession.commit()
        return obj.id;

    def get_measurement_types(self):
        query = DBSession.query(MeasurementConfig)
        return query.order_by(MeasurementConfig.label.asc()).all()
