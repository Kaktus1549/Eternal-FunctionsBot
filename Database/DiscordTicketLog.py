# Database/DiscordTicketLog.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from Database.Base import Base

class DiscordTicketLog(Base):
    __tablename__ = 'discord_tickets_logs'

    Ticket_ID = Column(Integer, ForeignKey('discord_tickets.Ticket_ID'), primary_key=True)
    Category = Column(String(255), nullable=True)
    Transcript = Column(Text, nullable=True)

    ticket = relationship("DiscordTicket", back_populates="log")
