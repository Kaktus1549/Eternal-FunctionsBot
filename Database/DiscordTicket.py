# Database/DiscordTicket.py
from sqlalchemy import Column, Integer, BigInteger, Boolean, Date, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Database.Base import Base

class DiscordTicket(Base):
    __tablename__ = 'discord_tickets'

    Ticket_ID = Column(Integer, primary_key=True, autoincrement=True)
    Discord_ID = Column(BigInteger, nullable=False)
    Opened = Column(Boolean, nullable=False, default=True)
    Open_Date = Column(Date, nullable=False, default=func.curdate())
    Claimed_by = Column(Text, nullable=True)

    log = relationship("DiscordTicketLog", back_populates="ticket", uselist=False)
