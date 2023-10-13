from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.infra.db import Base


class BudgetBreakdown(Base):
    # typed model
    __tablename__ = "budget_breakdown"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # create foreign key to users table
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    year: Mapped[int] = mapped_column()
    month: Mapped[int] = mapped_column()
    # jsonb column for storing the budget breakdown
    budget_breakdown: Mapped[dict] = mapped_column(JSONB())
    last_updated: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=True
    )


class User(Base):
    # auth0 user info model
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sub: Mapped[str] = mapped_column(index=True, unique=True)
    email: Mapped[str] = mapped_column(nullable=False)
    given_name: Mapped[str | None] = mapped_column(nullable=True)
    family_name: Mapped[str | None] = mapped_column(nullable=True)
    nickname: Mapped[str | None] = mapped_column(nullable=True)
    name: Mapped[str | None] = mapped_column(nullable=True)
    picture: Mapped[str | None] = mapped_column(nullable=True)
    locale: Mapped[str | None] = mapped_column(nullable=True)
    updated_at: Mapped[str | None] = mapped_column(nullable=True)
    email_verified: Mapped[bool | None] = mapped_column(nullable=True)
