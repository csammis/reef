from flask import jsonify
from flask.ext import restful
from flask.ext.restful import reqparse, abort
from endpoints import event_manager, try_get_time
import events

get_measurement_args = reqparse.RequestParser()
get_measurement_args.add_argument('parameter', type=str, action='append')
get_measurement_args.add_argument('start', type=str)
get_measurement_args.add_argument('end', type=str)

post_measurement_args = reqparse.RequestParser()
post_measurement_args.add_argument('type', type=str, required=True, help="'type' must be supplied")
post_measurement_args.add_argument('value', type=float, required=True, help="'value' must be supplied")
post_measurement_args.add_argument('time', type=str)

#
# Define a resource for lists of measurements
#
class MeasurementsResource(restful.Resource):

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

