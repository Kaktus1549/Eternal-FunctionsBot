# Database/Player.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from Database.Base import Base

class Player(Base):
    __tablename__ = 'Player'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    RoleId = Column(Integer, ForeignKey('Role.Id'), nullable=True)
    Username = Column(String(50), nullable=False, unique=True)
    UserId = Column(String(100), nullable=False, unique=True)
    DiscordId = Column(String(100), nullable=True)

    role = relationship("Role", back_populates="players")
    vip_assignments = relationship("VipAssignment", back_populates="player")
    activities = relationship("Activity", back_populates="player")
