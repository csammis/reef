from flask import jsonify
from flask.ext import restful
from flask.ext.restful import reqparse, abort
from endpoints import config_manager
import models

post_event_args = reqparse.RequestParser()
post_event_args.add_argument('event_name', type=str, required=True, help="'event_name' must be supplied")
post_event_args.add_argument('on_days[]', type=int, action='append', default=None)

class ScheduledEventResource(restful.Resource):
    
    def get(self, tank_name):
        tank = config_manager.get_tank_from_name(tank_name)
        if tank is None:
            abort(400, message="Tank with name '{}' not found".format(tank_name))
        return jsonify(schedule = config_manager.get_scheduled_events(tank.id))

    def post(self, tank_name):
        tank = config_manager.get_tank_from_name(tank_name)
        if tank is None:
            abort(400, message="Tank with name '{}' not found".format(tank_name))
        args = post_event_args.parse_args()
        if len(args['event_name']) == 0:
            abort(400, message="Required field 'event_name' cannot be blank")

        se = models.ScheduledEvent(tank.id, args['event_name'])
        days = args['on_days[]']
        if days is None:
            days = [] 
        se.on_sunday = True if 0 in days else False
        se.on_monday = True if 1 in days else False
        se.on_tuesday = True if 2 in days else False
        se.on_wednesday = True if 3 in days else False
        se.on_thursday = True if 4 in days else False
        se.on_friday = True if 5 in days else False
        se.on_saturday = True if 6 in days else False
        config_manager.add(se)
        return jsonify(schedule = se)

class ScheduledEventSingleResource(restful.Resource):

    def put(self, event_id):
        se = config_manager.get_scheduled_event(event_id)
        if se is None:
            abort(404, message="Scheduled event with ID {} not found".format(event_id))
        args = post_event_args.parse_args()
        days = args['on_days[]']
        if days is None:
            days = []
        update_dict = {}
        update_dict[models.ScheduledEvent.on_sunday] = True if 0 in days else False
        update_dict[models.ScheduledEvent.on_monday] = True if 1 in days else False
        update_dict[models.ScheduledEvent.on_tuesday] = True if 2 in days else False
        update_dict[models.ScheduledEvent.on_wednesday] = True if 3 in days else False
        update_dict[models.ScheduledEvent.on_thursday] = True if 4 in days else False
        update_dict[models.ScheduledEvent.on_friday] = True if 5 in days else False
        update_dict[models.ScheduledEvent.on_saturday] = True if 6 in days else False
        update_dict[models.ScheduledEvent.event_name] = args['event_name']
        config_manager.update_scheduled_event(event_id, update_dict)

        response = jsonify(schedule = config_manager.get_scheduled_event(event_id))
        response.status_code = 201
        return response

    def delete(self, event_id):
        se = config_manager.get_scheduled_event(event_id)
        if se is None:
            abort(404, message="Scheduled event with ID {} not found".format(event_id))
        config_manager.delete(se)
        return '', 204

class ScheduledEventAllResource(restful.Resource):
    def get(self):
        retval = []
        for tank in config_manager.get_tanks():
            retval.append({ 'name': tank.name, 'schedule': config_manager.get_scheduled_events(tank.id) })
        return jsonify(all = retval)
