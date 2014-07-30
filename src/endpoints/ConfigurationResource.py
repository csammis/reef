from flask import jsonify
from flask.ext import restful
from flask.ext.restful import reqparse, abort
from endpoints import config_manager
import models

post_measurement_config_args = reqparse.RequestParser()
post_measurement_config_args.add_argument('label', type=str, required=True, help="'label' must be supplied")
post_measurement_config_args.add_argument('units', type=str, default=None)
post_measurement_config_args.add_argument('acceptable_range[]', type=float, action='append', default=None)

class ConfigurationResource(restful.Resource):

    def get(self, config_type):
        if config_type == 'measurements':
            #configs = [];
            #configs.append(models.MeasurementConfig('Temperature', units = 'Degrees F', acceptable_range = [77, 82]))
            #configs.append(models.MeasurementConfig('Alkalinity', units = 'ppm CaCO3', acceptable_range = [125, 200]))
            #configs.append(models.MeasurementConfig('pH', acceptable_range = [8.1, 8.4]))
            #configs.append(models.MeasurementConfig('Phosphate', units = 'ppm'))
            #configs.append(models.MeasurementConfig('Calcium', units = 'ppm', acceptable_range = [420, 500]))
            #configs.append(models.MeasurementConfig('Specific Gravity', acceptable_range = [1.020, 1.025]))
            #configs.append(models.MeasurementConfig('Magnesium', units = 'ppm', acceptable_range = [1250, 1350]))
            
            return jsonify(configs = config_manager.get_measurement_types())

    def post(self, config_type):
        if config_type == 'measurements':
            args = post_measurement_config_args.parse_args()

            if len(args['label']) == 0:
                abort(400, message="Required field 'label' cannot be blank")

            config = models.MeasurementConfig(args['label'], units = args['units'], acceptable_range = args['acceptable_range[]'])
            return jsonify(measurement_type_id = config_manager.add(config))


class ConfigurationSingleResource(restful.Resource):

    def put(self, config_type, config_id):
        if config_type == 'measurements':
            args = post_measurement_config_args.parse_args()

            if len(args['label']) == 0:
                abort(400, message="Required field 'label' cannot be blank")

            config = config_manager.get_measurement_type(config_id)
            if config is None:
                abort(404, message='Measurement type with ID {} not found'.format(config_id))
            
            config_manager.update_measurement_type(config_id, args['label'], args['units'], args['acceptable_range[]'])
            config = config_manager.get_measurement_type(config_id)
            return { 'measurement_type': { 'id': config_id, 'label': config.label, 'units': config.units, 'acceptable_range': config.acceptable_range() } }, 201

    def get(self, config_type, config_id):
        if config_type == 'measurements':
            config = config_manager.get_measurement_type(config_id)
            if config is None:
                abort(404, message='Measurement type with ID {} not found'.format(config_id))
            return jsonify(measurement_type = config)
        return '', 404

    def delete(self, config_type, config_id):
        if config_type == 'measurements':
            config = config_manager.get_measurement_type(config_id)
            if config is None:
                abort(404, message='Measurement type with ID {} not found'.format(config_id))
            config_manager.delete(config)
        return '', 204

