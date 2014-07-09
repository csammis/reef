from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy import func
from events import Base

class Measurement(Base) :

    __tablename__ = 'Measurements'
    id = Column(Integer, primary_key = True)
    measurement_time = Column(DateTime, default=func.now())
    measurement_type = Column(Integer)
    value = Column(Float, nullable = True)

    ' Measurement types '
    PHOSPHATE, MAGNESIUM, CALCIUM, KH, PH, SPECIFICGRAVITY, TEMPERATURE, NITRATE = range(0, 8)

    def __init__(self, measurement_type, measurement_time = None, value = None) :
        self.measurement_type = measurement_type
        self.measurement_time = measurement_time
        self.value = value
 
