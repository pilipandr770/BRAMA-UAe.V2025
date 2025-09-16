from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from ..services.db import Base

class Meeting(Base):
    __tablename__ = "meetings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    starts_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    agenda_items = relationship("MeetingAgendaItem", back_populates="meeting", cascade="all, delete-orphan")
    votes = relationship("MeetingVote", back_populates="meeting", cascade="all, delete-orphan")

class MeetingAgendaItem(Base):
    __tablename__ = "meeting_agenda_items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meetings.id"))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    details: Mapped[str] = mapped_column(Text, default="")
    meeting = relationship("Meeting", back_populates="agenda_items")

class MeetingVote(Base):
    __tablename__ = "meeting_votes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meetings.id"))
    user_id: Mapped[int] = mapped_column(Integer)  # FK users.id спрощено
    agenda_item_id: Mapped[int] = mapped_column(Integer)  # FK meeting_agenda_items.id спрощено
    value: Mapped[int] = mapped_column(Integer, default=0)  # 1/0/-1
    meeting = relationship("Meeting", back_populates="votes")