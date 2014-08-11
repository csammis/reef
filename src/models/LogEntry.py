from sqlalchemy import Column, Integer, UnicodeText, DateTime, ForeignKey
from sqlalchemy import func
from sqlalchemy.orm import relationship
from models import Base

class LogEntry(Base) :

    __tablename__ = 'LogEntries'
    id = Column(Integer, primary_key = True)
    tank_id = Column(Integer, ForeignKey('Tank.id'))
    entry_time = Column(DateTime, index=True, default=func.now())
    entry = Column(UnicodeText, nullable = True)
    tank = relationship('Tank')

    def __init__(self, tank_id, entry, entry_time = None) :
        self.tank_id = tank_id
        self.entry = entry
        self.entry_time = entry_time
