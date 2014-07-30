from flask.ext import restful
from flask.ext.restful import abort
from datetime import datetime
from json import JSONEncoder
import dateutil.parser
import models

api = restful.Api()
models.initialize_sql('models/reefpi.db')
event_manager = models.EventManager()
config_manager = models.ConfigManager()

def try_get_time(args, key):
    try:
        return dateutil.parser.parse(args[key])
    except:
        abort(400, message="Unable to parse '{}' parameter '{}' into datetime".format(key, args[key]))

class ModelEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, models.Measurement):
            return {'id': o.id,\
                    'measurement_time': o.measurement_time,\
                    'measurement_type_id': o.measurement_type_id,\
                    'value': o.value}
        elif isinstance(o, models.LogEntry):
            return {'id': o.id,\
                    'entry_time': o.entry_time,\
                    'entry': o.entry}
        elif isinstance(o, models.MeasurementConfig):
            return {'id': o.id,\
                    'label': o.label,\
                    'units': o.units, \
                    'acceptable_range': o.acceptable_range()}
        elif isinstance(o, datetime):
            return o.isoformat()
        else:
            return JSONEncoder.default(self, o)


from endpoints import MeasurementResource
api.add_resource(MeasurementResource.MeasurementResource, '/measurements/')
api.add_resource(MeasurementResource.MeasurementSingleResource, '/measurements/<int:measurement_id>')
from endpoints import LogEntryResource
api.add_resource(LogEntryResource.LogEntryResource, '/logentries/')
api.add_resource(LogEntryResource.LogEntrySingleResource, '/logentries/<int:logentry_id>')
from endpoints import ConfigurationResource
api.add_resource(ConfigurationResource.ConfigurationResource, '/configs/<string:config_type>')
api.add_resource(ConfigurationResource.ConfigurationSingleResource, '/configs/<string:config_type>/<int:config_id>')


def register(app):
    api.init_app(app)
    app.json_encoder = ModelEncoder
