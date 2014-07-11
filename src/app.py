from flask import Flask
from flask import jsonify
from flask import request
from flask import abort
from datetime import datetime

import events

app = Flask(__name__)
event_manager = events.EventManager('events/events.db')

@app.route('/')
def index():
    return 'an index page here'

@app.route('/measurements/')
def measurements():
    return 'this is where all the pretty graphs might go'

@app.route('/measurements/<time_range>')
def get_measurements(time_range):
    if time_range == 'all':
        events = event_manager.get_measurements()
    elif time_range == 'range':
        try:
            start = int(request.args['start'])
            trange = (datetime.fromtimestamp(start),)
        except (KeyError, ValueError):
            abort(400)

        end = request.args.get('end', '')
        if end != '':
            try:
                trange += (datetime.fromtimestamp(int(end)),)
            except ValueError:
                abort(400)

        events = event_manager.get_measurements(trange)

    return jsonify(range = time_range, events = events)

@app.route('/measurements/add', methods=['POST'])
def add_measurement():
    pass

if __name__ == '__main__':
    app.run(debug=True)

