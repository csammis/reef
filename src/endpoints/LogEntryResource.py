from flask import jsonify
from flask.ext import restful
from flask.ext.restful import abort, reqparse
from endpoints import event_manager, try_get_time
import models

put_logentry_args = reqparse.RequestParser()
put_logentry_args.add_argument('entry', type=str, required=True, help="'entry' must be supplied")

get_logentry_args = reqparse.RequestParser()
get_logentry_args.add_argument('tank_id', type=int)
get_logentry_args.add_argument('start', type=str)
get_logentry_args.add_argument('end', type=str)

post_logentry_args = reqparse.RequestParser()
post_logentry_args.add_argument('tank_id', type=int, required=True, help="'tank_id' must be supplied")
post_logentry_args.add_argument('entry', type=str, required=True, help="'entry' must be supplied")
post_logentry_args.add_argument('time', type=str)

#
# Define a resource for lists of log entries
#
class LogEntryResource(restful.Resource):

    def get(self):
        args = get_logentry_args.parse_args()
        trange = {}
        if args['start'] is not None:
            trange['start'] = try_get_time(args, 'start')
        if args['end'] is not None:
            trange['end'] = try_get_time(args, 'end')

        return jsonify(logentries = event_manager.get_log_entries(tank_id = args['tank_id'], timerange = trange))

    def post(self):
        args = post_logentry_args.parse_args()
        entry_time = None
        if args['time'] is not None:
            entry_time = try_get_time(args, 'time')

        entry = args['entry'];
        if len(entry) == 0:
            abort(400, message="'entry' must be supplied")

        event = models.LogEntry(tank_id = args['tank_id'], entry_time = entry_time, entry = args['entry'])
        return jsonify(log_id = event_manager.add(event))

class LogEntrySingleResource(restful.Resource):

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

