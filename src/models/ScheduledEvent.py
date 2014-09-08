from sqlalchemy import Column, Integer, ForeignKey, UnicodeText, Boolean
from sqlalchemy.orm import relationship
from models import Base

class ScheduledEvent(Base):
    
    __tablename__ = 'ScheduledEvent'
    id = Column(Integer, primary_key = True)
    tank_id = Column(Integer, ForeignKey('Tank.id'), nullable = False)
    event_name = Column(UnicodeText, nullable = False)
    on_sunday = Column(Boolean, default = False)
    on_monday = Column(Boolean, default = False)
    on_tuesday = Column(Boolean, default = False)
    on_wednesday = Column(Boolean, default = False)
    on_thursday = Column(Boolean, default = False)
    on_friday = Column(Boolean, default = False)
    on_saturday = Column(Boolean, default = False)
    tank = relationship('Tank')

    def __init__(self, tank_id, event_name):
        self.tank_id = tank_id
        self.event_name = event_name
