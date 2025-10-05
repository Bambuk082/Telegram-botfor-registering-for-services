from database.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, BigInteger, String, DateTime, JSON, Boolean, func
from datetime import datetime

from typing import Optional

def get_weekday():
    return datetime.now().strftime('%A')

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    username: Mapped[str] = mapped_column(nullable=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    phone_number: Mapped[str] = mapped_column(String, nullable=True, unique=True, default=None)

    record_date: Mapped[str] = mapped_column(String, nullable=True, default=None, unique=False)

    status: Mapped[str] = mapped_column(String, nullable=False, default='user')
    is_admin: Mapped[bool] = mapped_column(default=False)

    registration_data: Mapped[dict] = mapped_column(JSON, default=None, nullable=True)
    registration_status: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    queue_message_to_back: Mapped[list] = mapped_column(JSON, nullable=True, default=[])
    queue_callback_registration_to_back: Mapped[list] = mapped_column(JSON, nullable=True, default=[])
    queue_registration_to_back: Mapped[list] = mapped_column(JSON, nullable=True, default=[])
    change_data: Mapped[list] = mapped_column(JSON, nullable=True, default=[])



