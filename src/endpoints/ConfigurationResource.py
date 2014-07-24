from flask import jsonify
from flask.ext import restful
import events

class ConfigurationResource(restful.Resource):

    def get(self, config_type):
        if config_type == 'measurements':
            configs = [];
            configs.append(events.MeasurementConfig(events.MeasurementType.Temperature, 'Temp', [78, 82], 'Degrees F'))
            configs.append(events.MeasurementConfig(events.MeasurementType.KH, 'Alkalinity', [125, 200], 'ppm CaCO3'))
            configs.append(events.MeasurementConfig(events.MeasurementType.PH, 'pH', [8.1, 8.4], ''))
            configs.append(events.MeasurementConfig(events.MeasurementType.Phosphate, value_label='parts per million'))
            configs.append(events.MeasurementConfig(events.MeasurementType.Calcium, value_range=[420, 500], value_label='parts per million'))
            configs.append(events.MeasurementConfig(events.MeasurementType.SpecificGravity, measurement_label='Specific gravity'))
            configs.append(events.MeasurementConfig(events.MeasurementType.Magnesium, value_range=[1250, 1350], value_label='parts per million'))

            configDict = {c.measurement_type.name: {'range': c.value_range, 'measurement_label': c.measurement_label, 'value_label': c.value_label } \
                    for c in configs}
            return jsonify(configs = configDict)

