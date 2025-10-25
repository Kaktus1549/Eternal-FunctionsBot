# Database/Activity.py
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from Database.Base import Base

class Activity(Base):
    __tablename__ = 'Activity'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    PlayerId = Column(Integer, ForeignKey('Player.Id'), nullable=False)
    TimeOnServerSeconds = Column(Integer, nullable=False, default=0)

    player = relationship("Player", back_populates="activities")
