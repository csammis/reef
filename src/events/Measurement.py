from sqlalchemy import Column, Integer, Float, DateTime, Enum
from sqlalchemy import func
from events import Base
from events import MeasurementType
from events import MeasurementTypeDecorator

class Measurement(Base) :

    __tablename__ = 'Measurements'
    id = Column(Integer, primary_key = True)
    measurement_time = Column(DateTime, index = True, default=func.now(), nullable = False)
    measurement_type = Column(MeasurementTypeDecorator.Enum3(MeasurementType.MeasurementType), nullable = False)
    value = Column(Float, nullable = True)

    def __init__(self, measurement_type, measurement_time = None, value = None) :
        self.measurement_type = measurement_type
        self.measurement_time = measurement_time
        self.value = value
 
