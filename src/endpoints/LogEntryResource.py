from flask import jsonify
from flask.ext import restful
from flask.ext.restful import abort, reqparse
from endpoints import event_manager

put_logentry_args = reqparse.RequestParser()
put_logentry_args.add_argument('entry', type=str, required=True, help="'entry' must be supplied")

class LogEntryResource(restful.Resource):

    def get(self, logentry_id):
        event = event_manager.get_log_entry(logentry_id)
        if event is None:
            abort(404, message='Log entry with ID {} not found'.format(logentry_id))
        return jsonify(logentry = event)

    def delete(self, logentry_id):
        event = event_manager.get_log_entry(logentry_id)
        if event is None:
            abort(404, message='Log entry with ID {} not found'.format(logentry_id))
        event_manager.delete(event);
        return '', 204

    def put(self, logentry_id):
        args = put_logentry_args.parse_args()
        event = event_manager.get_log_entry(logentry_id)
        if event is None:
            abort(404, message='Log entry with ID {} not found'.format(logentry_id))
        event_manager.update_log_entry(logentry_id, entry = args['entry'], entry_time = event.entry_time)
        event.entry = args['entry']
        return { 'entry' : {'id' : event.id, 'entry': event.entry, 'entry_time': event.entry_time.isoformat()} }, 201

