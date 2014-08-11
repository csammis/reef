from sqlalchemy import Column, Integer, UnicodeText
from models import Base

class Tank(Base):
    __tablename__ = 'Tank'

    id = Column(Integer, primary_key = True)
    name = Column(UnicodeText, nullable = False, unique = True)

    def __init__(self, name):
        self.name = name
