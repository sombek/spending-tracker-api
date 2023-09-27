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
        BudgetBreakdown.user_id == user.id,
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

    initial_budget = BudgetBreakdownJson.model_validate(
        {
            "money_in": [{"title": "Salary", "amount": 10500.0}],
            "multi_payments": [
                {
                    "x": 0,
                    "y": 0,
                    "title": "Bills",
                    "height": 117,
                    "purchases": [
                        {"title": "Electricty", "amount": 215.5},
                        {"title": "Internet", "amount": 287.5},
                    ],
                },
                {
                    "x": 2,
                    "y": 0,
                    "title": "\r\nGas\r\n",
                    "height": 94,
                    "purchases": [{"title": "26/09", "amount": 144.0}],
                },
                {
                    "x": 0,
                    "y": 117,
                    "title": "\r\nInternet Subscription\r\n",
                    "height": 163,
                    "purchases": [
                        {"title": "\r\nيوتيوب بيرميوم\r\n", "amount": 36.0},
                        {"title": "\r\nايكلاود\r\n", "amount": 45.0},
                        {"title": "1Password", "amount": 15.3},
                        {"title": "Google Storage", "amount": 6.99},
                    ],
                },
                {
                    "x": 1,
                    "y": 160,
                    "title": "\r\nGroceries\r\n",
                    "height": 117,
                    "purchases": [
                        {"title": "Tamimi", "amount": 250.0},
                        {"title": "مقاضي لعزيمة اهلي", "amount": 411.0},
                    ],
                },
                {
                    "x": 1,
                    "y": 0,
                    "title": "\r\nResturants & Cafes\r\n",
                    "height": 160,
                    "purchases": [
                        {"title": "فايف قايز مع الشباب", "amount": 67.0},
                        {"title": "غداء في الدوام من جاهز", "amount": 54.0},
                        {"title": "\r\nدوار السعادة\r\n", "amount": 23.0},
                    ],
                },
                {
                    "x": 2,
                    "y": 94,
                    "title": "Others",
                    "height": 246,
                    "purchases": [
                        {"title": "Coffee Beans", "amount": 103.0},
                        {"title": "Tickets to Riyadh Season", "amount": 250.0},
                        {
                            "title": "\r\nرسوم تحويل من STCPay to Bank\r\n",
                            "amount": 6.0,
                        },
                        {"title": "\r\nحلاق\r\n", "amount": 60.0},
                        {"title": "رسوم مواقف المطار يوم وصلت ريان", "amount": 20.0},
                    ],
                },
            ],
            "single_payments": [
                {"title": "Rent", "amount": 2000.0},
                {"title": "Charity", "amount": 250.0},
                {"title": "Loan", "amount": 1750.0},
                {"title": "Investment", "amount": 2500.0},
            ],
            "last_month_money_remaining": None,
        }
    )
    budget = BudgetBreakdown(
        year=year,
        month=month,
        user_id=user.id,
        budget_breakdown=initial_budget.model_dump(),
    )
    session.add(budget)
    session.commit()
    if last_month_remaining != 0:
        initial_budget.last_month_money_remaining = last_month_remaining

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
