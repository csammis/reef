from flask import Flask
from flask import jsonify
from flask import request
from flask import abort
from flask.ext import restful
from datetime import datetime
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

# Define a resource endpoint for measurements
class Measurements(restful.Resource):
    def get(self):
        trange = timerange_from_request()
        parameters = parameters_from_request()
        return jsonify(events = event_manager.get_measurements(parameters = parameters, timerange = trange))

api.add_resource(Measurements, '/measurements/')

if __name__ == '__main__':
    app.run(debug=True)

