from sqlalchemy import Column, Integer, String, Text
from database import Base

class Journal(Base):
    __tablename__ = "journals"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(String)
    ambience = Column(String)
    text = Column(Text)
    emotion = Column(String)