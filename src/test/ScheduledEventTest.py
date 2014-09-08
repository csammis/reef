import models

class TestScheduledEvent(object):
    
    @classmethod
    def setup_class(cls):
        models.initialize_sql(':memory:')
        cls._cm = models.ConfigManager()
        
        tank = models.Tank('TestTank')
        cls._cm.add(tank)
        cls._tank = tank

    def setup(self):
        models.DBSession.query(models.ScheduledEvent).delete()

    def test_add_scheduled_event(self):
        se = models.ScheduledEvent(TestScheduledEvent._tank.id, 'TestEvent')
        TestScheduledEvent._cm.add(se)
        assert se.id is not None
        assert se.on_sunday is False
        assert se.on_monday is False
        assert se.on_tuesday is False
        assert se.on_wednesday is False
        assert se.on_thursday is False
        assert se.on_friday is False
        assert se.on_saturday is False

    @classmethod
    def insert_scheduled_events(cls):
        cls._cm.add(models.ScheduledEvent(cls._tank.id, 'TestEvent2'))
        cls._cm.add(models.ScheduledEvent(cls._tank.id, 'TestEvent1'))
        cls._cm.add(models.ScheduledEvent(cls._tank.id, 'TestEvent3'))

    def test_get_scheduled_events(self):
        TestScheduledEvent.insert_scheduled_events()

        l = TestScheduledEvent._cm.get_scheduled_events(TestScheduledEvent._tank.id)
        assert len(l) == 3
        assert l[0].event_name < l[1].event_name and l[1].event_name < l[2].event_name

    def test_delete_scheduled_event(self):
        TestScheduledEvent.insert_scheduled_events()

        l = TestScheduledEvent._cm.get_scheduled_events(TestScheduledEvent._tank.id)
        TestScheduledEvent._cm.delete(l[0])
        l2 = TestScheduledEvent._cm.get_scheduled_events(TestScheduledEvent._tank.id)
        assert len(l2) == 2
