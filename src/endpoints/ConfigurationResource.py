from flask import jsonify
from flask.ext import restful
from flask.ext.restful import reqparse
from endpoints import config_manager
import events

post_measurement_config_args = reqparse.RequestParser()
post_measurement_config_args.add_argument('label', type=str, required=True, help="'label' must be supplied")
post_measurement_config_args.add_argument('units', type=str, default=None)
post_measurement_config_args.add_argument('acceptable_range[]', type=float, action='append', default=None)

class ConfigurationResource(restful.Resource):

    def get(self, config_type):
        if config_type == 'measurements':
            #configs = [];
            #configs.append(events.MeasurementConfig('Temperature', units = 'Degrees F', acceptable_range = [77, 82]))
            #configs.append(events.MeasurementConfig('Alkalinity', units = 'ppm CaCO3', acceptable_range = [125, 200]))
            #configs.append(events.MeasurementConfig('pH', acceptable_range = [8.1, 8.4]))
            #configs.append(events.MeasurementConfig('Phosphate', units = 'ppm'))
            #configs.append(events.MeasurementConfig('Calcium', units = 'ppm', acceptable_range = [420, 500]))
            #configs.append(events.MeasurementConfig('Specific Gravity', acceptable_range = [1.020, 1.025]))
            #configs.append(events.MeasurementConfig('Magnesium', units = 'ppm', acceptable_range = [1250, 1350]))
            
            return jsonify(configs = config_manager.get_measurement_types())

    def post(self, config_type):
        if config_type == 'measurements':
            args = post_measurement_config_args.parse_args()

            config = events.MeasurementConfig(args['label'], units = args['units'], acceptable_range = args['acceptable_range[]'])
            return jsonify(measurement_type_id = config_manager.add(config))


class ConfigurationSingleResource(restful.Resource):

    def put(self, config_type, config_id):
        pass

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

