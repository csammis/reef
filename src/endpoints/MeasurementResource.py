from flask import jsonify, send_file
from flask.ext import restful
from flask.ext.restful import abort, reqparse
from endpoints import event_manager, config_manager, try_get_time
import models
from resources import ParameterImage
from io import BytesIO

get_measurement_args = reqparse.RequestParser()
get_measurement_args.add_argument('measurement_type_id', type=int, action='append')
get_measurement_args.add_argument('tank_id', type=int, required=True, help="'tank_id' must be supplied")
get_measurement_args.add_argument('start', type=str)
get_measurement_args.add_argument('end', type=str)
get_measurement_args.add_argument('as_of', type=str)

post_measurement_args = reqparse.RequestParser()
post_measurement_args.add_argument('tank_id', type=int, required=True, help="'tank_id' must be supplied")
post_measurement_args.add_argument('measurement_type_id', type=int, required=True, help="'measurement_type_id' must be supplied")
post_measurement_args.add_argument('value', type=float, required=True, help="'value' must be supplied")
post_measurement_args.add_argument('time', type=str)

#
# Define a resource for lists of measurements
#
class MeasurementResource(restful.Resource):

    def get(self):
        args = get_measurement_args.parse_args()
        parameters = args['measurement_type_id']
        trange = {}
        if args['as_of'] is None:
            if args['start'] is not None:
                trange['start'] = try_get_time(args, 'start')
            if args['end'] is not None:
                trange['end'] = try_get_time(args, 'end')
            return jsonify(measurements = event_manager.get_measurements(parameters = parameters, tank_id = args['tank_id'], timerange = trange))

        else:
            as_of = try_get_time(args, 'as_of')
            pimg = ParameterImage.ParameterImage()
            return send_file(pimg.get_image_stream(args['tank_id'], as_of), mimetype='image/png')

    def post(self):
        args = post_measurement_args.parse_args()

        measurement_type = config_manager.get_measurement_type(args['measurement_type_id'])
        if measurement_type is None:
            abort(400, message="Measurement type with ID '{}' is not valid".format(args['measurement_type_id']))

        measurement_time = None
        if args['time'] is not None:
            measurement_time = try_get_time(args, 'time')

        event = models.Measurement(tank_id = args['tank_id'], measurement_type_id = measurement_type.id, measurement_time = measurement_time, value = args['value'])
        event_manager.add(event)
        return jsonify(event = event)


#
# Define a resource for dealing with a single measurement
#
class MeasurementSingleResource(restful.Resource):

    def get(self, measurement_id):
        event = event_manager.get_measurement(measurement_id)
        if event is None:
            abort(404, message='Measurement with ID {} not found'.format(measurement_id))
        return jsonify(event = event)

