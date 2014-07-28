from flask.ext import restful
from flask.ext.restful import abort
from datetime import datetime
from json import JSONEncoder
import dateutil.parser
import events

api = restful.Api()
events.initialize_sql('events/events.db')
event_manager = events.EventManager()

def try_get_time(args, key):
    try:
        return dateutil.parser.parse(args[key])
    except:
        abort(400, message="Unable to parse '{}' parameter '{}' into datetime".format(key, args[key]))

class EventsEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, events.Measurement):
            return {'id': o.id,\
                    'measurement_time': o.measurement_time,\
                    'measurement_type': o.measurement_type.name,\
                    'value': o.value}
        elif isinstance(o, events.LogEntry):
            return {'id': o.id,\
                    'entry_time': o.entry_time,\
                    'entry': o.entry}
        elif isinstance(o, events.MeasurementConfig):
            return {'id': o.id,\
                    'label': o.label,\
                    'units': o.units, \
                    'acceptable_range': o.acceptable_range()}
        elif isinstance(o, datetime):
            return o.isoformat()
        else:
            return JSONEncoder.default(self, o)


from endpoints import MeasurementsResource
api.add_resource(MeasurementsResource.MeasurementsResource, '/measurements/')
from endpoints import MeasurementResource
api.add_resource(MeasurementResource.MeasurementResource, '/measurements/<int:measurement_id>')
from endpoints import LogEntriesResource
api.add_resource(LogEntriesResource.LogEntriesResource, '/logentries/')
from endpoints import LogEntryResource
api.add_resource(LogEntryResource.LogEntryResource, '/logentries/<int:logentry_id>')
from endpoints import ConfigurationResource
api.add_resource(ConfigurationResource.ConfigurationResource, '/configs/<string:config_type>')


def register(app):
    api.init_app(app)
    app.json_encoder = EventsEncoder
