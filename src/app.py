from flask import Flask
from flask import jsonify
from flask import request
from flask.ext.restful import abort
from flask.ext import restful
from datetime import datetime
from json import JSONEncoder
import events

app = Flask(__name__)
api = restful.Api(app)
event_manager = events.EventManager('events/events.db')

@app.route('/')
def index():
    return 'an index page here'

@app.route('/parameters/')
def parameters():
    return 'this is where all the pretty graphs might go'

class EventsEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, events.Measurement):
            return {'id': o.id,\
                    'measurement_time': o.measurement_time,\
                    'measurement_type': o.measurement_type,\
                    'value': o.value}
        else:
            return JSONEncoder.default(self, o)

app.json_encoder = EventsEncoder 

def timerange_from_request():
    trange = { }
    try:
        if 'start' in request.args.keys():
            start = int(request.args['start'])
            trange['start'] = datetime.fromtimestamp(start)
    except ValueError:
        abort(400)

    try:
        if 'end' in request.args.keys():
            end = int(request.args['end'])
            trange['end'] = datetime.fromtimestamp(end)
    except ValueError:
        abort(400)

    return trange

def parameters_from_request():
    parameters = None
    if 'parameters' in request.args.keys():
        parameters = request.args['parameters'].split(',')
    return parameters

# Define a resource for lists of measurements
class Measurements(restful.Resource):
    def get(self):
        trange = timerange_from_request()
        parameters = parameters_from_request()
        return jsonify(events = event_manager.get_measurements(parameters = parameters, timerange = trange))

api.add_resource(Measurements, '/measurements/')

# Define a resource for dealing with a single measurement
class Measurement(restful.Resource):
    def get(self, measurement_id):
        event = event_manager.get_measurement(measurement_id)
        if event is None:
            abort(404, message='Measurement with ID {} not found'.format(measurement_id))
        return jsonify(event = event)

api.add_resource(Measurement, '/measurements/<int:measurement_id>')

if __name__ == '__main__':
    app.run(debug=True)

