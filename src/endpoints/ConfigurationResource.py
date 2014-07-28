from flask import jsonify
from flask.ext import restful
import events

class ConfigurationResource(restful.Resource):

    def get(self, config_type):
        if config_type == 'measurements':
            configs = [];
            configs.append(events.MeasurementConfig('Temperature', units = 'Degrees F', acceptable_range = [77, 82]))
            configs.append(events.MeasurementConfig('Alkalinity', units = 'ppm CaCO3', acceptable_range = [125, 200]))
            configs.append(events.MeasurementConfig('pH', acceptable_range = [8.1, 8.4]))
            configs.append(events.MeasurementConfig('Phosphate', units = 'ppm'))
            configs.append(events.MeasurementConfig('Calcium', units = 'ppm', acceptable_range = [420, 500]))
            configs.append(events.MeasurementConfig('Specific Gravity', acceptable_range = [1.020, 1.025]))
            configs.append(events.MeasurementConfig('Magnesium', units = 'ppm', acceptable_range = [1250, 1350]))

            return jsonify(configs = configs)

