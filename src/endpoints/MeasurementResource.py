from flask import jsonify
from flask.ext import restful
from flask.ext.restful import abort
from endpoints import event_manager

#
# Define a resource for dealing with a single measurement
#
class MeasurementResource(restful.Resource):

    def get(self, measurement_id):
        event = event_manager.get_measurement(measurement_id)
        if event is None:
            abort(404, message='Measurement with ID {} not found'.format(measurement_id))
        return jsonify(event = event)

