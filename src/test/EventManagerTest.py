import events
import datetime

class TestEventManager(object):

    @classmethod
    def setup_class(cls):
        cls._em = events.EventManager(':memory:')

    def setup(self):
        events.DBSession.query(events.Measurement).delete()

    def test_add_measurement_implicit_time(self):
        m = events.Measurement(events.Measurement.CALCIUM)
        m.value = 472
        TestEventManager._em.add(m)

        l = TestEventManager._em.get_measurements()
        assert len(l) == 1
        assert type(l[0]) is events.Measurement
        assert l[0].value == 472
        assert l[0].measurement_time == m.measurement_time

    def test_add_measurement_explicit_time(self):
        m = events.Measurement(events.Measurement.CALCIUM)
        m.value = 472
        m.measurement_time = datetime.datetime.fromtimestamp(123456)
        TestEventManager._em.add(m)

        l = TestEventManager._em.get_measurements()
        assert len(l) == 1
        assert l[0].measurement_time == datetime.datetime.fromtimestamp(123456)


