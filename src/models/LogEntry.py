from sqlalchemy import Column, Integer, UnicodeText, DateTime
from sqlalchemy import func
from models import Base

class LogEntry(Base) :

    __tablename__ = 'LogEntries'
    id = Column(Integer, primary_key = True)
    entry_time = Column(DateTime, index=True, default=func.now())
    entry = Column(UnicodeText, nullable = True)

    def __init__(self, entry, entry_time = None) :
        self.entry = entry
        self.entry_time = entry_time
