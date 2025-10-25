# Database/VipAssignment.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from Database.Base import Base

class VipAssignment(Base):
    __tablename__ = 'VipAssignment'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    PlayerId = Column(Integer, ForeignKey('Player.Id'), nullable=False)
    VipRoleId = Column(Integer, ForeignKey('VipRole.Id'), nullable=False)
    SpawnHumanCount = Column(Integer, nullable=True)
    SpawnScpCount = Column(Integer, nullable=True)
    AssignedAt = Column(DateTime, default=datetime.utcnow)

    player = relationship("Player", back_populates="vip_assignments")
    vip_role = relationship("VipRole", back_populates="assignments")
