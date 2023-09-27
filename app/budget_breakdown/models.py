from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.budget_breakdown.schemas import BudgetBreakdownJson
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


class User(Base):
    # auth0 user info model
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sub: Mapped[str] = mapped_column(index=True, unique=True)
    email: Mapped[str] = mapped_column()
    given_name: Mapped[str | None] = mapped_column()
    family_name: Mapped[str | None] = mapped_column()
    nickname: Mapped[str | None] = mapped_column()
    name: Mapped[str | None] = mapped_column()
    picture: Mapped[str | None] = mapped_column()
    locale: Mapped[str | None] = mapped_column()
    updated_at: Mapped[str | None] = mapped_column()
    email_verified: Mapped[bool | None] = mapped_column()
