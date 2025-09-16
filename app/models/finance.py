from sqlalchemy import Integer, String, Text, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from ..services.db import Base

class Transaction(Base):
    """
    Платежі учасників, витрати на проєкти — загальний журнал.
    type: 'income' | 'expense'
    """
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String(16), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(8), default="EUR")
    description: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)