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
