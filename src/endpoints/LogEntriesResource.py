from flask import jsonify
from flask.ext import restful
from flask.ext.restful import reqparse, abort
from endpoints import event_manager, try_get_time
import events

get_logentry_args = reqparse.RequestParser()
get_logentry_args.add_argument('start', type=str)
get_logentry_args.add_argument('end', type=str)

post_logentry_args = reqparse.RequestParser()
post_logentry_args.add_argument('entry', type=str, required=True, help="'entry' must be supplied")
post_logentry_args.add_argument('time', type=str)

#
# Define a resource for lists of log entries
#
class LogEntriesResource(restful.Resource):

    def get(self):
        args = get_logentry_args.parse_args()
        trange = {}
        if args['start'] is not None:
            trange['start'] = try_get_time(args, 'start')
        if args['end'] is not None:
            trange['end'] = try_get_time(args, 'end')

        return jsonify(logentries = event_manager.get_log_entries(timerange = trange))

    def post(self):
        args = post_logentry_args.parse_args()
        entry_time = None
        if args['time'] is not None:
            entry_time = try_get_time(args, 'time')

        entry = args['entry'];
        if len(entry) == 0:
            abort(400, message="'entry' must be supplied")

        event = events.LogEntry(entry_time = entry_time, entry = args['entry'])
        return jsonify(log_id = event_manager.add(event))

