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

    last_month_sum_money_in = 0
    last_month_sum_money_out = 0
    last_month_remaining = 0

    last_month_budget_stmt = select(BudgetBreakdown).where(
        BudgetBreakdown.year == year,
        BudgetBreakdown.month == month - 1,
    )
    last_month_budget = session.execute(last_month_budget_stmt).scalar_one_or_none()
    if last_month_budget is not None:
        parsed_budget = BudgetBreakdownJson.model_validate(
            last_month_budget.budget_breakdown
        )
        for moneyIn in parsed_budget.money_in:
            if moneyIn.amount is not None:
                last_month_sum_money_in += moneyIn.amount
        for single_payment in parsed_budget.single_payments:
            if single_payment.amount is not None:
                last_month_sum_money_out += single_payment.amount
        for multi_payment in parsed_budget.multi_payments:
            for purchases in multi_payment.purchases:
                if purchases.amount is not None:
                    last_month_sum_money_out += purchases.amount

        last_month_remaining = last_month_sum_money_in - last_month_sum_money_out

    if budget:
        if last_month_remaining != 0:
            budget.budget_breakdown["last_month_money_remaining"] = last_month_remaining
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
