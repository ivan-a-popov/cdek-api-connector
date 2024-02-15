from datetime import datetime
from typing import Optional
from sqlalchemy.types import UUID
from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column


Base = declarative_base()

class Delivery(Base):
    """DB model for Delivery"""
    __tablename__ = "delivery_api"
    id: Mapped[BigInteger] = mapped_column(BigInteger, primary_key=True) # ForeignKey('order.id'),
    crm_id: Mapped[int] = mapped_column()
    tk_name: Mapped[str] = mapped_column()
    tk_id: Mapped[Optional[str]] = mapped_column()
    tk_status: Mapped[Optional[str]] = mapped_column()
    tk_uuid: Mapped[Optional[UUID]] = mapped_column(UUID)
    updated: Mapped[Optional[datetime]] = mapped_column()
    print_file: Mapped[Optional[str]] = mapped_column()
