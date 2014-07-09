import sqlite3

class MeasurementRepository(object) :

    def __init__(self) :
        super(MeasurementRepository, self).__init__()
        self._conn = sqlite3.connect("events.db")

    def add(self, measurement) :
        if measurement.has_value :
            self._conn.execute("INSERT INTO Measurement VALUES(?)", measurement.measurement_type)
        else :
            self._conn.execute("INSERT INTO Measurement VALUES(?, ?, ?)", measurement.time, measurement.measurement_type, measurement.value)

