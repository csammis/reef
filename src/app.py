from flask import Flask, jsonify, request, url_for, render_template
from flask.ext.restful import abort, reqparse
from flask.ext import restful
from datetime import datetime
import dateutil.parser
from json import JSONEncoder
import events

app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
api = restful.Api(app)
event_manager = events.EventManager('events/events.db')

@app.route('/')
def index():
    return render_template('index.html', title='Reef')

@app.route('/parameters/')
def parameters():
    return render_template('parameters.html', \
            title='Parameters', \
            libraries=['jquery','d3'], \
            stylesheet=url_for('static', filename='main.css'), \
            script=url_for('static', filename='parameters.js'))

@app.route('/parameters/add/')
def add_parameters():
    return render_template('add_parameters.html')

@app.route('/logs/')
def logs():
    return render_template('logs.html', \
            title='Logs', \
            libraries=['jquery','jquery-ui'], \
            stylesheet=url_for('static', filename='logs.css'),
            script=url_for('static', filename='logs.js'))

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
        elif isinstance(o, datetime):
            return o.isoformat()
        else:
            return JSONEncoder.default(self, o)

app.json_encoder = EventsEncoder 

#
# Parameter parsing
#
post_measurement_args = reqparse.RequestParser()
post_measurement_args.add_argument('type', type=str, required=True, help="'type' must be supplied")
post_measurement_args.add_argument('value', type=float, required=True, help="'value' must be supplied")
post_measurement_args.add_argument('time', type=str)

get_measurement_args = reqparse.RequestParser()
get_measurement_args.add_argument('parameter', type=str, action='append')
get_measurement_args.add_argument('start', type=str)
get_measurement_args.add_argument('end', type=str)

get_logentry_args = reqparse.RequestParser()
get_logentry_args.add_argument('start', type=str)
get_logentry_args.add_argument('end', type=str)

post_logentry_args = reqparse.RequestParser()
post_logentry_args.add_argument('entry', type=str, required=True, help="'entry' must be supplied")
post_logentry_args.add_argument('time', type=str)

put_logentry_args = reqparse.RequestParser()
put_logentry_args.add_argument('entry', type=str, required=True, help="'entry' must be supplied")

def try_get_time(args, key):
    try:
        return dateutil.parser.parse(args[key])
    except:
        abort(400, message="Unable to parse '{}' parameter '{}' into datetime".format(key, args[key]))

#
# Define a resource for lists of measurements
#
class Measurements(restful.Resource):

    def get(self):
        args = get_measurement_args.parse_args()
        parameters = args['parameter']
        trange = {}
        if args['start'] is not None:
            trange['start'] = try_get_time(args, 'start')
        if args['end'] is not None:
            trange['end'] = try_get_time(args, 'end')

        return jsonify(events = event_manager.get_measurements(parameters = parameters, timerange = trange))

    def post(self):
        args = post_measurement_args.parse_args()
        try:
            measurement_type = events.MeasurementType[args['type']]
        except KeyError:
            abort(400, message="Measurement type '{}' is not valid".format(args['type']))

        measurement_time = None
        if args['time'] is not None:
            measurement_time = try_get_time(args, 'time')

        event = events.Measurement(measurement_type = measurement_type, measurement_time = measurement_time, value = args['value'])
        return jsonify(measurement_id = event_manager.add(event))

api.add_resource(Measurements, '/measurements/')

#
# Define a resource for dealing with a single measurement
#
class Measurement(restful.Resource):

    def get(self, measurement_id):
        event = event_manager.get_measurement(measurement_id)
        if event is None:
            abort(404, message='Measurement with ID {} not found'.format(measurement_id))
        return jsonify(event = event)

api.add_resource(Measurement, '/measurements/<int:measurement_id>')

#
# Define a resource for lists of log entries
#
class LogEntries(restful.Resource):

    def get(self):
        args = get_logentry_args.parse_args()
        trange = {}
        if args['start'] is not None:
            trange['start'] = try_get_time(args, 'start')
        if args['end'] is not None:
            trange['end'] = try_get_time(args, 'end')

        return jsonify(logentries = event_manager.get_log_entries(timerange = trange))

    def post(self):
        args = post_logentry_args.parse_args()
        entry_time = None
        if args['time'] is not None:
            entry_time = try_get_time(args, 'time')

        entry = args['entry'];
        if len(entry) == 0:
            abort(400, message="'entry' must be supplied")

        event = events.LogEntry(entry_time = entry_time, entry = args['entry'])
        return jsonify(log_id = event_manager.add(event))

api.add_resource(LogEntries, '/logentries/')

class LogEntry(restful.Resource):

    def get(self, logentry_id):
        event = event_manager.get_log_entry(logentry_id)
        if event is None:
            abort(404, message='Log entry with ID {} not found'.format(logentry_id))
        return jsonify(logentry = event)

    def delete(self, logentry_id):
        event = event_manager.get_log_entry(logentry_id)
        if event is None:
            abort(404, message='Log entry with ID {} not found'.format(logentry_id))
        event_manager.delete(event);
        return '', 204

    def put(self, logentry_id):
        args = put_logentry_args.parse_args()
        event = event_manager.get_log_entry(logentry_id)
        if event is None:
            abort(404, message='Log entry with ID {} not found'.format(logentry_id))
        event_manager.update_log_entry(logentry_id, entry = args['entry'], entry_time = event.entry_time)
        event.entry = args['entry']
        return { 'entry' : {'id' : event.id, 'entry': event.entry, 'entry_time': event.entry_time.isoformat()} }, 201

api.add_resource(LogEntry, '/logentries/<int:logentry_id>')

#
# Config testing pieces
#

class Config(restful.Resource):

    def get(self, config_type):
        if config_type == 'measurements':
            configs = [];
            configs.append(events.MeasurementConfig(events.MeasurementType.Temperature, 'Temp', [78, 82], 'Degrees F'))
            configs.append(events.MeasurementConfig(events.MeasurementType.KH, 'Alkalinity', [125, 200], 'ppm CaCO3'))
            configs.append(events.MeasurementConfig(events.MeasurementType.PH, 'pH', [8.1, 8.4], ''))
            configs.append(events.MeasurementConfig(events.MeasurementType.Phosphate, value_label='parts per million'))
            configs.append(events.MeasurementConfig(events.MeasurementType.Calcium, value_range=[420, 500], value_label='parts per million'))
            configs.append(events.MeasurementConfig(events.MeasurementType.SpecificGravity, measurement_label='Specific gravity'))
            configs.append(events.MeasurementConfig(events.MeasurementType.Magnesium, value_range=[1250, 1350], value_label='parts per million'))

            configDict = {c.measurement_type.name: {'range': c.value_range, 'measurement_label': c.measurement_label, 'value_label': c.value_label } \
                    for c in configs}
            return jsonify(configs = configDict)

api.add_resource(Config, '/configs/<string:config_type>')

if __name__ == '__main__':
    app.run(debug=True)

