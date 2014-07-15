
class MeasurementConfig(object) :

    def __init__(self, measurement_type, measurement_label, value_range, value_label) :
        self.measurement_type = measurement_type
        self.value_range = value_range
        self.measurement_label = measurement_label
        self.value_label = value_label

