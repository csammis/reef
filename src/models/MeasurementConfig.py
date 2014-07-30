from sqlalchemy import Column, Integer, Float, UnicodeText
from models import Base

class MeasurementConfig(Base):

    __tablename__ = 'MeasurementType'
    id = Column(Integer, primary_key=True)
    label = Column(UnicodeText, nullable=False)
    units = Column(UnicodeText, nullable=True)
    acceptable_range_low = Column(Float, nullable=True)
    acceptable_range_high = Column(Float, nullable=True)

    def __init__(self, label, units = None, acceptable_range = None) :
        self.label = label
        self.units = units
        self.acceptable_range_low = min(acceptable_range) if acceptable_range is not None else None
        self.acceptable_range_high = max(acceptable_range) if acceptable_range is not None else None

    def acceptable_range(self):
        return [self.acceptable_range_low, self.acceptable_range_high] if self.acceptable_range_low is not None else None
