from flask import jsonify
from flask.ext import restful
from flask.ext.restful import abort, reqparse
from endpoints import event_manager, try_get_time
import models

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
class MeasurementResource(restful.Resource):

    def get(self):
        args = get_measurement_args.parse_args()
        parameters = args['parameter']
        trange = {}
        if args['start'] is not None:
            trange['start'] = try_get_time(args, 'start')
        if args['end'] is not None:
            trange['end'] = try_get_time(args, 'end')

        return jsonify(models = event_manager.get_measurements(parameters = parameters, timerange = trange))

    def post(self):
        args = post_measurement_args.parse_args()
        try:
            measurement_type = models.MeasurementType[args['type']]
        except KeyError:
            abort(400, message="Measurement type '{}' is not valid".format(args['type']))

        measurement_time = None
        if args['time'] is not None:
            measurement_time = try_get_time(args, 'time')

        event = models.Measurement(measurement_type = measurement_type, measurement_time = measurement_time, value = args['value'])
        return jsonify(measurement_id = event_manager.add(event))


#
# Define a resource for dealing with a single measurement
#
class MeasurementSingleResource(restful.Resource):

    def get(self, measurement_id):
        event = event_manager.get_measurement(measurement_id)
        if event is None:
            abort(404, message='Measurement with ID {} not found'.format(measurement_id))
        return jsonify(event = event)

