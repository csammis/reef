import events
from events.MeasurementType import MeasurementType
import datetime

class TestEventManager(object):

    @classmethod
    def setup_class(cls):
        cls._em = events.EventManager(':memory:')

    def setup(self):
        events.DBSession.query(events.Measurement).delete()
        events.DBSession.query(events.LogEntry).delete()

    def test_add_measurement_implicit_time(self):
        m = events.Measurement(MeasurementType.Calcium)
        m.value = 472
        TestEventManager._em.add(m)

        l = TestEventManager._em.get_measurements()
        assert len(l) == 1
        assert type(l[0]) is events.Measurement
        assert l[0].value == 472
        assert l[0].measurement_time == m.measurement_time

    def test_add_measurement_explicit_time(self):
        m = events.Measurement(MeasurementType.Calcium)
        m.value = 472
        m.measurement_time = datetime.datetime.fromtimestamp(123456)
        TestEventManager._em.add(m)

        l = TestEventManager._em.get_measurements()
        assert len(l) == 1
        assert l[0].measurement_time == datetime.datetime.fromtimestamp(123456)

    @classmethod
    def insert_measurements(cls):
        dt = datetime.datetime
        TestEventManager._em.add(events.Measurement(MeasurementType.Calcium, dt.fromtimestamp(123456), 472))
        TestEventManager._em.add(events.Measurement(MeasurementType.Phosphate, dt.fromtimestamp(433563), 0.00))
        TestEventManager._em.add(events.Measurement(MeasurementType.KH, dt.fromtimestamp(32242), 7.33))

    def test_get_measurements_all(self):
        TestEventManager.insert_measurements()
        
        l = TestEventManager._em.get_measurements()
        assert len(l) == 3
        assert l[0].measurement_time < l[1].measurement_time and l[1].measurement_time < l[2].measurement_time

    def test_get_measurement(self):
        TestEventManager.insert_measurements()

        l = TestEventManager._em.get_measurements()
        measurement_id = l[0].id

        m = TestEventManager._em.get_measurement(measurement_id)
        assert m is not None
        assert m.measurement_time == l[0].measurement_time
        assert m.measurement_type == l[0].measurement_type
        assert m.value == l[0].value

    def test_get_measurement_not_found(self):
        TestEventManager.insert_measurements()

        m = TestEventManager._em.get_measurement(-1)
        assert m is None

    def test_get_measurements_with_parameters(self):
        TestEventManager.insert_measurements()

        l = TestEventManager._em.get_measurements(parameters = [MeasurementType.Calcium, MeasurementType.KH])
        assert len(l) == 2
        assert l[0].measurement_type == MeasurementType.KH
        assert l[1].measurement_type == MeasurementType.Calcium

    def test_get_measurements_greaterthan_time(self):
        TestEventManager.insert_measurements()
        
        l = TestEventManager._em.get_measurements(timerange = {'start': datetime.datetime.fromtimestamp(100000)})
        assert len(l) == 2
        assert l[0].measurement_time < l[1].measurement_time

    def test_get_measurements_between_time(self):
        TestEventManager.insert_measurements()

        trange = {'start': datetime.datetime.fromtimestamp(20), 'end': datetime.datetime.fromtimestamp(75000)}
        l = TestEventManager._em.get_measurements(timerange = trange)
        assert len(l) == 1
        assert l[0].value == 7.33
        assert l[0].measurement_type == MeasurementType.KH

    def test_get_measurements_lessthan_time(self):
        TestEventManager.insert_measurements()

        l = TestEventManager._em.get_measurements(timerange = {'end': datetime.datetime.fromtimestamp(100000)})
        assert len(l) == 1
        assert l[0].value == 7.33
        assert l[0].measurement_type == MeasurementType.KH

    def test_add_logentry_implicit_time(self):
        le = events.LogEntry('Hi there')
        TestEventManager._em.add(le)

        l = TestEventManager._em.get_log_entries()
        assert len(l) == 1
        assert l[0].entry == 'Hi there'
        assert l[0].entry_time == le.entry_time

    def test_add_logentry_explicit_time(self):
        le = events.LogEntry('Oh hello', datetime.datetime.fromtimestamp(123456))
        TestEventManager._em.add(le)

        l = TestEventManager._em.get_log_entries()
        assert len(l) == 1
        assert l[0].entry_time == datetime.datetime.fromtimestamp(123456)

    @classmethod
    def insert_log_entries(cls):
        dt = datetime.datetime
        TestEventManager._em.add(events.LogEntry('abc', dt.fromtimestamp(123456)))
        TestEventManager._em.add(events.LogEntry('def', dt.fromtimestamp(454335)))
        TestEventManager._em.add(events.LogEntry('ghi', dt.fromtimestamp(34432)))

    def test_get_logentry_all(self):
        TestEventManager.insert_log_entries()

        l = TestEventManager._em.get_log_entries()
        assert len(l) == 3
        assert l[0].entry_time < l[1].entry_time and l[1].entry_time < l[2].entry_time

    def test_get_logentry_greaterthan_time(self):
        TestEventManager.insert_log_entries()

        trange = {'start': datetime.datetime.fromtimestamp(100000)}
        l = TestEventManager._em.get_log_entries(trange)
        assert len(l) == 2
        assert l[0].entry_time < l[1].entry_time

    def test_get_logentry_between_time(self):
        TestEventManager.insert_log_entries()

        trange = {'start': datetime.datetime.fromtimestamp(20), 'end': datetime.datetime.fromtimestamp(75000)}
        l = TestEventManager._em.get_log_entries(trange)
        assert len(l) == 1
        assert l[0].entry == 'ghi'

    def test_get_logentry_lessthan_time(self):
        TestEventManager.insert_log_entries()

        trange = {'end': datetime.datetime.fromtimestamp(100000)}
        l = TestEventManager._em.get_log_entries(trange)
        assert len(l) == 1
        assert l[0].entry == 'ghi'
