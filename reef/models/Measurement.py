""" A Measurement (id, tank, measurement_type, measurement_time, value) """
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import func
from models import Base

class Measurement(Base):
    """ The ORM object for a Measurement """

    __tablename__ = 'Measurements'
    id = Column(Integer, primary_key=True)
    tank_id = Column(Integer, ForeignKey('Tank.id'), nullable=False)
    measurement_type_id = Column(Integer, ForeignKey('MeasurementType.id'))
    measurement_time = Column(DateTime, index=True, default=func.now(), nullable=False)
    value = Column(Float, nullable=True)
    measurement_type = relationship('MeasurementType')
    tank = relationship('Tank')

    def __init__(self, tank_id, measurement_type_id, measurement_time=None, value=None):
        self.tank_id = tank_id
        self.measurement_type_id = measurement_type_id
        self.measurement_time = measurement_time
        self.value = value
