import events

class TestConfigManager(object):

    @classmethod
    def setup_class(cls):
        events.initialize_sql(':memory:')
        cls._cm = events.ConfigManager()

    def setup(self):
        events.DBSession.query(events.MeasurementConfig).delete()

    def test_add_measurement_type(self):
        m = events.MeasurementConfig('Test')
        TestConfigManager._cm.add(m)

        l = TestConfigManager._cm.get_measurement_types()
        assert len(l) == 1
        assert type(l[0]) is events.MeasurementConfig
        assert l[0].label == 'Test'
        assert l[0].units is None
    
    @classmethod
    def insert_measurement_types(cls):
        TestConfigManager._cm.add(events.MeasurementConfig('Test C', units = 'ppm'))
        TestConfigManager._cm.add(events.MeasurementConfig('Test A'))
        TestConfigManager._cm.add(events.MeasurementConfig('Test B', units = 'ppb', acceptable_range = [12, 63]))

    def test_get_measurement_types(self):
        TestConfigManager.insert_measurement_types()

        l = TestConfigManager._cm.get_measurement_types()
        assert len(l) == 3
        assert l[0].label < l[1].label and l[1].label < l[2].label

    def test_get_measurement_type(self):
        TestConfigManager.insert_measurement_types()

        l = TestConfigManager._cm.get_measurement_types()

        mt = TestConfigManager._cm.get_measurement_type(l[0].id)
        assert mt is not None
        assert mt.label == l[0].label
        assert mt.units == l[0].units

    def test_update_measurement_type(self):
        TestConfigManager.insert_measurement_types()

        l = TestConfigManager._cm.get_measurement_types()
        assert l[0].label == 'Test A'
        assert l[0].units is None
        assert l[0].acceptable_range() is None

        TestConfigManager._cm.update_measurement_type(l[0].id, 'Update Test', 'mg', acceptable_range = [3, 5])
        mt = TestConfigManager._cm.get_measurement_type(l[0].id)
        assert mt.label == 'Update Test'
        assert mt.units == 'mg'
        assert mt.acceptable_range_low == 3
        assert mt.acceptable_range_high == 5

    def test_delete_measurement_type(self):
        TestConfigManager.insert_measurement_types()

        l = TestConfigManager._cm.get_measurement_types()
        assert len(l) == 3

        TestConfigManager._cm.delete(l[0])
        l2 = TestConfigManager._cm.get_measurement_types()
        assert len(l2) == 2
