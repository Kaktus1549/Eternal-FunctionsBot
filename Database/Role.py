# Database/Role.py
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from Database.Base import Base

class Role(Base):
    __tablename__ = 'Role'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    FullName = Column(String(100), nullable=False)
    ShortName = Column(String(50), nullable=False, unique=True)
    LogActivity = Column(Boolean, nullable=False, default=True)

    vip_roles = relationship("VipRole", back_populates="role")
    players = relationship("Player", back_populates="role")
