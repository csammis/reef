
class MeasurementConfig(object) :

    def __init__(self, measurement_type, measurement_label = None, value_range = None, value_label = None) :
        self.measurement_type = measurement_type
        self.value_range = value_range
        self.measurement_label = measurement_label
        self.value_label = value_label

