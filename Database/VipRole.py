# Database/VipRole.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from Database.Base import Base

class VipRole(Base):
    __tablename__ = 'VipRole'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Role_Id = Column(Integer, ForeignKey('Role.Id'), nullable=False)
    Name = Column(String(50), nullable=False, unique=True)
    DefaultHumanSpawns = Column(Integer, nullable=False)
    DefaultScpSpawns = Column(Integer, nullable=False)

    role = relationship("Role", back_populates="vip_roles")
    assignments = relationship("VipAssignment", back_populates="vip_role")
