import time

class Measurement(object) :

    ' Measurement types '
    PHOSPHATE, MAGNESIUM, CALCIUM, KH, PH, SPECIFICGRAVITY, TEMPERATURE, NITRATE = range(0, 8)

    def __init__(self) :
        self._hasvalue = False
        self._time = None
        super(Measurement, self).__init__()

    
    @property
    def value(self) :
        return self._value if self._hasvalue else None

    @value.setter
    def value(self, typeValue) :
        try :
            measurementType, value = typeValue
        except ValueError :
            raise ValueError("Pass both measurement type and value")

        self._type = measurementType 
        self._value = value
        self._hasvalue = True
        self.time = time.time()

    @property
    def has_value(self) :
        return self._hasvalue

    @property
    def measurement_type(self) :
        return self._type if self._hasvalue else None

    @property
    def time(self) :
        return self._time

    @time.setter
    def time(self, time) :
        self._time = time
