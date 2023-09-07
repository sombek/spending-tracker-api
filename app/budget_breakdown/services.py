from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.budget_breakdown.models import BudgetBreakdown, User
from app.budget_breakdown.schemas import BudgetBreakdownJson, Transaction


def get_budget_(
    year: int,
    month: int,
    session: Session,
    user: User,
) -> BudgetBreakdownJson:
    get_budget_query = select(BudgetBreakdown).where(
        BudgetBreakdown.year == year,
        BudgetBreakdown.month == month,
        BudgetBreakdown.user_id == user.id,
    )
    budget = session.execute(get_budget_query).scalar_one_or_none()
    if budget:
        return BudgetBreakdownJson.model_validate(budget.budget_breakdown)

    initial_budget = BudgetBreakdownJson(
        money_in=[
            Transaction(title="Salary", amount=0),
        ],
        single_payments=[
            Transaction(title="Rent", amount=0),
        ],
        multi_payments=[
            BudgetBreakdownJson.MultiPaymentBreakdown(
                title="Groceries",
                purchases=[
                    Transaction(title="Tamimi", amount=0),
                ],
            ),
        ],
    )
    budget = BudgetBreakdown(
        year=year,
        month=month,
        user_id=user.id,
        budget_breakdown=initial_budget.model_dump(),
    )
    session.add(budget)
    session.commit()
    return initial_budget


def upsert_budget_(
    year: int,
    month: int,
    budget_breakdown: BudgetBreakdownJson,
    session: Session,
    user: User,
) -> BudgetBreakdownJson:
    budget_query = select(BudgetBreakdown).where(
        BudgetBreakdown.year == year,
        BudgetBreakdown.month == month,
        BudgetBreakdown.user_id == user.id,
    )
    budget = session.execute(budget_query).scalar_one_or_none()
    if budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")

    budget.budget_breakdown = budget_breakdown.model_dump()
    session.commit()

    return budget_breakdown
