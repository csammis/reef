""" Endpoints for the scheduled event model object """
from flask import jsonify
from flask.ext import restful
from flask.ext.restful import reqparse, abort
from endpoints import config_manager
import models

post_event_args = reqparse.RequestParser()
post_event_args.add_argument('event_name', type=str, required=True, help="'event_name' must be supplied")
post_event_args.add_argument('on_days[]', type=int, action='append', default=None)

class ScheduledEventResource(restful.Resource):
    """ GET and POST for /schedule/ """

    def get(self, tank_name):
        """ GET /schedule/<tank_name> """
        tank = config_manager.get_tank_from_name(tank_name)
        if tank is None:
            abort(400, message="Tank with name '{}' not found".format(tank_name))
        return jsonify(schedule=config_manager.get_scheduled_events(tank.id))

    def post(self, tank_name):
        """ POST /schedule/<tank_name> """
        tank = config_manager.get_tank_from_name(tank_name)
        if tank is None:
            abort(400, message="Tank with name '{}' not found".format(tank_name))
        args = post_event_args.parse_args()
        if len(args['event_name']) == 0:
            abort(400, message="Required field 'event_name' cannot be blank")

        event = models.ScheduledEvent(tank.id, args['event_name'])
        days = args['on_days[]']
        if days is None:
            days = []
        event.on_sunday = True if 0 in days else False
        event.on_monday = True if 1 in days else False
        event.on_tuesday = True if 2 in days else False
        event.on_wednesday = True if 3 in days else False
        event.on_thursday = True if 4 in days else False
        event.on_friday = True if 5 in days else False
        event.on_saturday = True if 6 in days else False
        config_manager.add(event)
        return jsonify(schedule=event)

class ScheduledEventSingleResource(restful.Resource):
    """ PUT and DELETE for a single scheduled event """

    def put(self, event_id):
        """ PUT /schedule/<event_id> """
        test_event = config_manager.get_scheduled_event(event_id)
        if test_event is None:
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

        response = jsonify(schedule=config_manager.get_scheduled_event(event_id))
        response.status_code = 201
        return response

    def delete(self, event_id):
        """ DELETE /schedule/<event_id> """
        event = config_manager.get_scheduled_event(event_id)
        if event is None:
            abort(404, message="Scheduled event with ID {} not found".format(event_id))
        config_manager.delete(event)
        return '', 204

class ScheduledEventAllResource(restful.Resource):
    """ GET all scheduled events for all tanks from a single call """

    def get(self):
        """ GET /schedule/ """
        retval = []
        for tank in config_manager.get_tanks():
            retval.append({'name': tank.name, 'schedule': config_manager.get_scheduled_events(tank.id)})
        return jsonify(all=retval)
