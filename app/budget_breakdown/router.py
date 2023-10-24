# create router

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import validate_token_and_get_user
from app.infra.db import db_session
from .models import User, BudgetBreakdown

from .schemas import BudgetBreakdownJson, CamelModel
from .services import get_budget_, upsert_budget_

router = APIRouter()


@router.get(
    "/{year}/{month}",
    response_model=BudgetBreakdownJson,
)
def get_budget(
    year: int,
    month: int,
    session: Session = Depends(db_session),
    user: User = Depends(validate_token_and_get_user),
):
    return get_budget_(year, month, session, user)


class UserBudgets(CamelModel):
    year: int
    months: list[BudgetBreakdownJson]


def get_budgets_(session: Session, user: User):
    stmt = (
        session.query(BudgetBreakdown)
        .filter(BudgetBreakdown.user_id == user.id)
        .order_by(BudgetBreakdown.year, BudgetBreakdown.month)
    )
    budgets = stmt.all()
    user_budgets: list[UserBudgets] = []
    for budget in budgets:
        # find the year in the list
        year = next(
            (
                user_budget
                for user_budget in user_budgets
                if user_budget.year == budget.year
            ),
            None,
        )
        if year is None:
            year = UserBudgets(year=budget.year, months=[])
            user_budgets.append(year)

        year.months.append(get_budget_(budget.year, budget.month, session, user))

    return user_budgets


@router.get("", response_model=list[UserBudgets])
def get_budgets(
    session: Session = Depends(db_session),
    user: User = Depends(validate_token_and_get_user),
):
    return get_budgets_(session, user)


@router.delete("/{year}/{month}")
def delete_budget(
    year: int,
    month: int,
    session: Session = Depends(db_session),
    user: User = Depends(validate_token_and_get_user),
):
    stmt = (
        session.query(BudgetBreakdown)
        .filter(BudgetBreakdown.user_id == user.id)
        .filter(BudgetBreakdown.year == year)
        .filter(BudgetBreakdown.month == month)
    )
    stmt.delete()
    session.commit()
    return {"message": "Budget deleted successfully"}


@router.post(
    "/{year}/{month}",
    response_model=BudgetBreakdownJson,
)
def upsert_budget(
    year: int,
    month: int,
    budget_breakdown: BudgetBreakdownJson,
    session: Session = Depends(db_session),
    user: User = Depends(validate_token_and_get_user),
):
    return upsert_budget_(year, month, budget_breakdown, session, user)
