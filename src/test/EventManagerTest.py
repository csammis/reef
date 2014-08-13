import models
import datetime
from sqlalchemy.exc import IntegrityError

class TestEventManager(object):

    @classmethod
    def setup_class(cls):
        models.initialize_sql(':memory:')
        cls._em = models.EventManager()
        cls._cm = models.ConfigManager()
        
        mt1 = models.MeasurementType('Calcium', units = 'ppm')
        mt2 = models.MeasurementType('Phosphate', units = 'ppm')
        mt3 = models.MeasurementType('KH', units = 'ppm CaCO3')
        cls._cm.add(mt1)
        cls._cm.add(mt2)
        cls._cm.add(mt3)

        cls._mtypes = {'calcium': mt1.id, 'phosphate': mt2.id, 'KH': mt3.id}

        tank = models.Tank('DefaultTank')
        cls._cm.add(tank)
        cls._tank = tank

    def setup(self):
        models.DBSession.query(models.Measurement).delete()
        models.DBSession.query(models.LogEntry).delete()
        models.DBSession.query(models.Tank).filter(models.Tank.name != 'DefaultTank').delete()

    # Still can't believe I have to write this test
    def test_sqlite_fk_support_on(self):
        TestEventManager.insert_measurements()

        try:
            TestEventManager._cm.delete(TestEventManager._tank)
            assert False, 'Deletion failed despite foreign key constraint'
        except IntegrityError:
            assert True
        except:
            assert False, 'Deletion failed but threw exception other than IntegrityError'
        finally:
            models.DBSession.rollback()

    def test_add_measurement_implicit_time(self):
        m = models.Measurement(TestEventManager._tank.id, TestEventManager._mtypes['calcium'])
        m.value = 472
        TestEventManager._em.add(m)

        l = TestEventManager._em.get_measurements()
        assert len(l) == 1
        assert type(l[0]) is models.Measurement
        assert l[0].value == 472
        assert l[0].measurement_time == m.measurement_time

    def test_add_measurement_explicit_time(self):
        m = models.Measurement(TestEventManager._tank.id, TestEventManager._mtypes['calcium'])
        m.value = 472
        m.measurement_time = datetime.datetime.fromtimestamp(123456)
        TestEventManager._em.add(m)

        l = TestEventManager._em.get_measurements()
        assert len(l) == 1
        assert l[0].measurement_time == datetime.datetime.fromtimestamp(123456)

    @classmethod
    def insert_measurements(cls):
        dt = datetime.datetime
        TestEventManager._em.add(models.Measurement(cls._tank.id, cls._mtypes['calcium'], dt.fromtimestamp(123456), 472))
        TestEventManager._em.add(models.Measurement(cls._tank.id, cls._mtypes['phosphate'], dt.fromtimestamp(433563), 0.00))
        TestEventManager._em.add(models.Measurement(cls._tank.id, cls._mtypes['KH'], dt.fromtimestamp(32242), 7.33))

    @classmethod
    def insert_measurements_for_tank(cls, tankname):
        dt = datetime.datetime
        tank = models.Tank(tankname)
        cls._cm.add(tank)

        TestEventManager._em.add(models.Measurement(tank.id, cls._mtypes['calcium'], dt.fromtimestamp(1234256), 242))
        TestEventManager._em.add(models.Measurement(tank.id, cls._mtypes['phosphate'], dt.fromtimestamp(4363563), 0.40))
        TestEventManager._em.add(models.Measurement(tank.id, cls._mtypes['KH'], dt.fromtimestamp(322452), 8.33))

        return tank.id

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
        assert m.measurement_type_id == l[0].measurement_type_id
        assert m.measurement_type.label == l[0].measurement_type.label
        assert m.value == l[0].value

    def test_get_measurement_not_found(self):
        TestEventManager.insert_measurements()

        m = TestEventManager._em.get_measurement(-1)
        assert m is None

    def test_get_measurements_with_parameters(self):
        TestEventManager.insert_measurements()

        l = TestEventManager._em.get_measurements(parameters = [TestEventManager._mtypes['calcium'], TestEventManager._mtypes['KH']])
        assert len(l) == 2
        assert l[0].measurement_type_id == TestEventManager._mtypes['KH']
        assert l[1].measurement_type_id == TestEventManager._mtypes['calcium']

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
        assert l[0].measurement_type_id == TestEventManager._mtypes['KH']

    def test_get_measurements_lessthan_time(self):
        TestEventManager.insert_measurements()

        l = TestEventManager._em.get_measurements(timerange = {'end': datetime.datetime.fromtimestamp(100000)})
        assert len(l) == 1
        assert l[0].value == 7.33
        assert l[0].measurement_type_id == TestEventManager._mtypes['KH']

    def test_delete_measurement(self):
        TestEventManager.insert_measurements()

        l = TestEventManager._em.get_measurements()
        TestEventManager._em.delete(l[0])

        assert len(TestEventManager._em.get_measurements()) == 2

    def test_get_measurements_with_tank_id(self):
        TestEventManager.insert_measurements()
        tank_id = TestEventManager.insert_measurements_for_tank('Second tank')

        l = TestEventManager._em.get_measurements()
        assert len(l) == 6

        l2 = TestEventManager._em.get_measurements(tank_id = tank_id)
        assert len(l2) == 3

        l3 = TestEventManager._em.get_measurements(tank_id = TestEventManager._tank.id)
        assert len(l3) == 3

        assert l3[0].id != l2[0].id

    def test_add_logentry_implicit_time(self):
        le = models.LogEntry(TestEventManager._tank.id, 'Hi there')
        TestEventManager._em.add(le)

        l = TestEventManager._em.get_log_entries()
        assert len(l) == 1
        assert l[0].entry == 'Hi there'
        assert l[0].entry_time == le.entry_time

    def test_add_logentry_explicit_time(self):
        le = models.LogEntry(TestEventManager._tank.id, 'Oh hello', datetime.datetime.fromtimestamp(123456))
        TestEventManager._em.add(le)

        l = TestEventManager._em.get_log_entries()
        assert len(l) == 1
        assert l[0].entry_time == datetime.datetime.fromtimestamp(123456)

    @classmethod
    def insert_log_entries(cls):
        dt = datetime.datetime
        TestEventManager._em.add(models.LogEntry(TestEventManager._tank.id, 'abc', dt.fromtimestamp(123456)))
        TestEventManager._em.add(models.LogEntry(TestEventManager._tank.id, 'def', dt.fromtimestamp(454335)))
        TestEventManager._em.add(models.LogEntry(TestEventManager._tank.id, 'ghi', dt.fromtimestamp(34432)))

    @classmethod
    def insert_log_entries_for_tank(cls, tankname):
        dt = datetime.datetime

        tank = models.Tank(tankname)
        cls._cm.add(tank)

        TestEventManager._em.add(models.LogEntry(tank.id, 'pqr', dt.fromtimestamp(12347856)))
        TestEventManager._em.add(models.LogEntry(tank.id, 'mno', dt.fromtimestamp(4547335)))
        TestEventManager._em.add(models.LogEntry(tank.id, 'jkl', dt.fromtimestamp(344532)))

        return tank.id

    def test_get_logentry_all(self):
        TestEventManager.insert_log_entries()

        l = TestEventManager._em.get_log_entries()
        assert len(l) == 3
        assert l[0].entry_time < l[1].entry_time and l[1].entry_time < l[2].entry_time

    def test_get_logentry(self):
        TestEventManager.insert_log_entries()

        l = TestEventManager._em.get_log_entries()
        assert len(l) == 3
        e = TestEventManager._em.get_log_entry(l[0].id)
        assert e is not None
        assert e.id == l[0].id
        assert e.entry_time == l[0].entry_time
        assert e.entry == l[0].entry

    def test_get_logentry_not_found(self):
        TestEventManager.insert_log_entries()

        e = TestEventManager._em.get_log_entry(-1)
        assert e is None

    def test_get_logentry_greaterthan_time(self):
        TestEventManager.insert_log_entries()

        trange = {'start': datetime.datetime.fromtimestamp(100000)}
        l = TestEventManager._em.get_log_entries(timerange = trange)
        assert len(l) == 2
        assert l[0].entry_time < l[1].entry_time

    def test_get_logentry_between_time(self):
        TestEventManager.insert_log_entries()

        trange = {'start': datetime.datetime.fromtimestamp(20), 'end': datetime.datetime.fromtimestamp(75000)}
        l = TestEventManager._em.get_log_entries(timerange = trange)
        assert len(l) == 1
        assert l[0].entry == 'ghi'

    def test_get_logentry_lessthan_time(self):
        TestEventManager.insert_log_entries()

        trange = {'end': datetime.datetime.fromtimestamp(100000)}
        l = TestEventManager._em.get_log_entries(timerange = trange)
        assert len(l) == 1
        assert l[0].entry == 'ghi'

    def test_delete_logentry(self):
        TestEventManager.insert_log_entries()

        l = TestEventManager._em.get_log_entries()
        TestEventManager._em.delete(l[0])

        assert len(TestEventManager._em.get_log_entries()) == 2

    def test_update_logentry(self):
        TestEventManager.insert_log_entries()

        l = TestEventManager._em.get_log_entries()
        assert l[0].entry == 'ghi'
        TestEventManager._em.update_log_entry(l[0].id, 'xyz', l[0].entry_time)

        e = TestEventManager._em.get_log_entry(l[0].id)
        assert e.entry == 'xyz'

    def test_get_logentry_with_tank_id(self):
        TestEventManager.insert_log_entries()
        tank_id = TestEventManager.insert_log_entries_for_tank('Second tank')

        l = TestEventManager._em.get_log_entries()
        assert len(l) == 6

        l2 = TestEventManager._em.get_log_entries(tank_id = TestEventManager._tank.id)
        assert len(l2) == 3

        l3 = TestEventManager._em.get_log_entries(tank_id = tank_id)
        assert len(l3) == 3

        assert l2[0].id != l3[0].id

