""" Endpoints for site configuration """
from flask import jsonify
from flask.ext import restful
from flask.ext.restful import reqparse, abort
from endpoints import config_manager
import models

post_measurement_config_args = reqparse.RequestParser()
post_measurement_config_args.add_argument('label', type=str, required=True, help="'label' must be supplied")
post_measurement_config_args.add_argument('units', type=str, default=None)
post_measurement_config_args.add_argument('acceptable_range[]', type=float, action='append', default=None)

post_tank_config_args = reqparse.RequestParser()
post_tank_config_args.add_argument('name', type=str, required=True, help="'name' must be supplied")

class ConfigurationResource(restful.Resource):
    """ GET and POST for site configurations """

    def get(self, config_type):
        """ GET /configs/<config_type> """
        if config_type == 'measurements':
            return jsonify(configs=config_manager.get_measurement_types())
        elif config_type == 'tanks':
            return jsonify(tanks=config_manager.get_tanks())
        else:
            return '', 404

    def post(self, config_type):
        """ POST /configs/<config_type> """
        if config_type == 'measurements':
            args = post_measurement_config_args.parse_args()

            if len(args['label']) == 0:
                abort(400, message="Required field 'label' cannot be blank")

            config = models.MeasurementType(args['label'], units=args['units'], acceptable_range=args['acceptable_range[]'])
            config_manager.add(config)
            return jsonify(measurement_type=config)
        elif config_type == 'tanks':
            args = post_tank_config_args.parse_args()

            if len(args['name']) == 0:
                abort(400, message="Required field 'name' cannot be blank")

            tank = models.Tank(args['name'])
            config_manager.add(tank)
            return jsonify(tank=tank)
        else:
            return '', 404


class ConfigurationSingleResource(restful.Resource):
    """ PUT, GET, and DELETE for a single site configuration """

    def put(self, config_type, config_id):
        """ PUT /configs/<config_type>/<config_id> """
        if config_type == 'measurements':
            args = post_measurement_config_args.parse_args()

            if len(args['label']) == 0:
                abort(400, message="Required field 'label' cannot be blank")

            config = config_manager.get_measurement_type(config_id)
            if config is None:
                abort(404, message='Measurement type with ID {} not found'.format(config_id))

            config_manager.update_measurement_type(config_id, args['label'], args['units'], args['acceptable_range[]'])
            config = config_manager.get_measurement_type(config_id)
            response = jsonify(measurement_type=config)
            response.status_code = 201
            return response
        elif config_type == 'tanks':
            args = post_tank_config_args.parse_args()

            if len(args['name']) == 0:
                abort(400, message="Required field 'name' cannot be blank")

            tank = config_manager.get_tank(config_id)
            if tank is None:
                abort(404, message='Tank with ID {} not found'.format(config_id))

            config_manager.update_tank(config_id, args['name'])
            tank = config_manager.get_tank(config_id)
            response = jsonify(tank=tank)
            response.status_code = 201
            return response
        else:
            return '', 404

    def get(self, config_type, config_id):
        """ GET /configs/<config_type>/<config_id> """
        if config_type == 'measurements':
            config = config_manager.get_measurement_type(config_id)
            if config is None:
                abort(404, message='Measurement type with ID {} not found'.format(config_id))
            return jsonify(measurement_type=config)
        elif config_type == 'tanks':
            tank = config_manager.get_tank(config_id)
            if tank is None:
                abort(404, message='Tank with ID {} not found'.format(config_id))
            return jsonify(tank=tank)
        else:
            return '', 404

    def delete(self, config_type, config_id):
        """ DELETE /configs/<config_type>/<config_id> """
        config = None
        if config_type == 'measurements':
            config = config_manager.get_measurement_type(config_id)
        elif config_type == 'tanks':
            config = config_manager.get_tank(config_id)

        if config is None:
            return '', 404

        try:
            config_manager.delete(config)
        except models.InUseException:
            return {'message': 'Cannot delete configuration: object is in use.'.format(config_id)}, 409
        return '', 204

