""" Setup and utility methods for the Flask-RESTful API """
import flask_restful
from flask_restful import abort
from datetime import datetime
from json import JSONEncoder
import dateutil.parser
import models

api = flask_restful.Api()
models.initialize_sql('reefpi.db')
event_manager = models.EventManager()
config_manager = models.ConfigManager()

def try_parse_time(date):
    """ Attempt to parse a time and abort HTTP 400 if dateutil can't figure it out """
    try:
        return dateutil.parser.parse(date)
    except ValueError:
        abort(400, message="Unable to parse '{}' into datetime".format(date))

def try_get_time(args, key):
    """ Attempt to get and parse a time from a dict, aborting HTTP 400 if the key is not present """
    try:
        return try_parse_time(args[key])
    except KeyError:
        abort(400, message="Unable to parse '{}' parameter into datetime: no such parameter was supplied".format(key))

class ModelEncoder(JSONEncoder):
    """ Custom JSON encoder for objects in the models module """
    def default(self, o):
        json = None
        if isinstance(o, models.Measurement):
            json = {'id': o.id,
                    'tank_id': o.tank_id,
                    'measurement_time': o.measurement_time,
                    'measurement_type_id': o.measurement_type_id,
                    'value': o.value}
        elif isinstance(o, models.LogEntry):
            json = {'id': o.id,
                    'tank_id': o.tank_id,
                    'entry_time': o.entry_time,
                    'entry': o.entry}
        elif isinstance(o, models.MeasurementType):
            json = {'id': o.id,
                    'label': o.label,
                    'units': o.units,
                    'acceptable_range': o.acceptable_range()}
        elif isinstance(o, models.Tank):
            json = {'id': o.id,
                    'name': o.name}
        elif isinstance(o, models.ScheduledEvent):
            json = {'id': o.id,
                    'event_name': o.event_name,
                    'on_days': {
                        'monday': o.on_monday,
                        'tuesday': o.on_tuesday,
                        'wednesday': o.on_wednesday,
                        'thursday': o.on_thursday,
                        'friday': o.on_friday,
                        'saturday': o.on_saturday,
                        'sunday': o.on_sunday}}
        elif isinstance(o, datetime):
            json = o.isoformat()
        else:
            json = JSONEncoder.default(self, o)
        return json


from endpoints import MeasurementResource
api.add_resource(MeasurementResource.MeasurementResource,
                 '/measurements/')
api.add_resource(MeasurementResource.MeasurementSingleResource,
                 '/measurements/<int:measurement_id>')
api.add_resource(MeasurementResource.MeasurementImageResource,
                 '/measurements/<string:tank_name>/<string:as_of>')

from endpoints import ScheduledEventResource
api.add_resource(ScheduledEventResource.ScheduledEventAllResource,
                 '/schedule/')
api.add_resource(ScheduledEventResource.ScheduledEventSingleResource,
                 '/schedule/<int:event_id>')
api.add_resource(ScheduledEventResource.ScheduledEventResource,
                 '/schedule/<string:tank_name>')

from endpoints import LogEntryResource
api.add_resource(LogEntryResource.LogEntryResource,
                 '/logentries/')
api.add_resource(LogEntryResource.LogEntrySingleResource,
                 '/logentries/<int:logentry_id>')

from endpoints import ConfigurationResource
api.add_resource(ConfigurationResource.ConfigurationResource,
                 '/configs/<string:config_type>')
api.add_resource(ConfigurationResource.ConfigurationSingleResource,
                 '/configs/<string:config_type>/<int:config_id>')


def register(app):
    """ Register the Flask-RESTful API with the Flask app and set up the custom JSON encoder """
    api.init_app(app)
    app.json_encoder = ModelEncoder
