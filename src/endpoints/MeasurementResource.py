""" Endpoints for the tank parameter measurement model object and related features """
from flask import jsonify, send_file
from flask.ext import restful
from flask.ext.restful import abort, reqparse
from endpoints import event_manager, config_manager, try_get_time, try_parse_time
import models
from resources import ParameterImage

get_measurement_args = reqparse.RequestParser()
get_measurement_args.add_argument('measurement_type_id', type=int, action='append')
get_measurement_args.add_argument('tank_id', type=int, required=True, help="'tank_id' must be supplied")
get_measurement_args.add_argument('start', type=str)
get_measurement_args.add_argument('end', type=str)

post_measurement_args = reqparse.RequestParser()
post_measurement_args.add_argument('tank_id', type=int, required=True, help="'tank_id' must be supplied")
post_measurement_args.add_argument('measurement_type_id', type=int, required=True, help="'measurement_type_id' must be supplied")
post_measurement_args.add_argument('value', type=float, required=True, help="'value' must be supplied")
post_measurement_args.add_argument('time', type=str)

class MeasurementResource(restful.Resource):
    """ GET and POST for lists of measurements """

    def get(self):
        """ GET /measurements/ """
        args = get_measurement_args.parse_args()
        parameters = args['measurement_type_id']
        trange = {}
        if args['start'] is not None:
            trange['start'] = try_get_time(args, 'start')
        if args['end'] is not None:
            trange['end'] = try_get_time(args, 'end')
        return jsonify(measurements=event_manager.get_measurements(parameters=parameters, tank_id=args['tank_id'], timerange=trange))

    def post(self):
        """ POST /measurements/ """
        args = post_measurement_args.parse_args()

        measurement_type = config_manager.get_measurement_type(args['measurement_type_id'])
        if measurement_type is None:
            abort(400, message="Measurement type with ID '{}' is not valid".format(args['measurement_type_id']))

        measurement_time = None
        if args['time'] is not None:
            measurement_time = try_get_time(args, 'time')

        event = models.Measurement(tank_id=args['tank_id'], measurement_type_id=measurement_type.id, measurement_time=measurement_time, value=args['value'])
        event_manager.add(event)
        return jsonify(event=event)

class MeasurementImageResource(restful.Resource):
    """ A resource for returning an image showing parameters as-of a date """

    def get(self, tank_name, as_of):
        """ GET /measurements/<tank_name>/<as_of> """
        as_of_date = try_parse_time(as_of)
        tank = config_manager.get_tank_from_name(tank_name)
        if tank is None:
            abort(400, message="Tank with name '{}' not found".format(tank_name))
        pimg = ParameterImage.ParameterImage()
        return send_file(pimg.get_image_stream(tank.id, as_of_date), mimetype='image/png')

class MeasurementSingleResource(restful.Resource):
    """ GET for a single measurement """

    def get(self, measurement_id):
        """ GET /measurements/<measurement_id> """
        event = event_manager.get_measurement(measurement_id)
        if event is None:
            abort(404, message='Measurement with ID {} not found'.format(measurement_id))
        return jsonify(event=event)

