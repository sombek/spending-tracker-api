from datetime import datetime

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

    last_month_sum_money_in = 0.0
    last_month_sum_money_out = 0.0
    last_month_remaining = 0.0

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
        budget.budget_breakdown["show_tour"] = False
        if last_month_remaining != 0:
            budget.budget_breakdown["last_month_money_remaining"] = last_month_remaining
        return BudgetBreakdownJson.model_validate(
            {
                **budget.budget_breakdown,
                "year": year,
                "month": month,
            }
        )

    initial_budget = BudgetBreakdownJson.model_validate(
        {
            "money_in": [
                {"title": "🏢 Salary", "amount": 14000},
                {"title": "Refund From Amazon", "amount": 24.77},
                {"title": "Stocks dividends", "amount": 3741.24},
                {"title": "Refund Medical Insurance", "amount": 350},
            ],
            "show_tour": True,
            "to_salary": None,
            "from_salary": None,
            "multi_payments": [
                {
                    "color": "blue",
                    "title": "⛽️ Gas",
                    "height": 117,
                    "columns": {
                        "1": {"x": 0, "y": 0},
                        "2": {"x": 0, "y": 0},
                        "3": {"x": 2, "y": 390},
                        "4": {"x": 3, "y": 0},
                        "5": {"x": 3, "y": 0},
                        "6": {"x": 0, "y": 0},
                        "7": {"x": 0, "y": 0},
                    },
                    "purchases": [
                        {"title": "Add Date", "amount": 141},
                        {"title": "Second Time?", "amount": 151.3},
                    ],
                },
                {
                    "color": "blue",
                    "title": "🧾 Bills",
                    "height": 140,
                    "columns": {
                        "1": {"x": 0, "y": 395},
                        "2": {"x": 1, "y": 278},
                        "3": {"x": 2, "y": 250},
                        "4": {"x": 1, "y": 0},
                        "5": {"x": 2, "y": 0},
                        "6": {"x": 1, "y": 0},
                        "7": {"x": 1, "y": 0},
                    },
                    "purchases": [
                        {"title": "\r\nالكهرباء\r\n", "amount": 410.6},
                        {"title": "Gym Bill", "amount": 99},
                        {"title": "Mobile Bill", "amount": 184},
                    ],
                },
                {
                    "color": "blue",
                    "title": "🌐 Internet Subscription",
                    "height": 250,
                    "columns": {
                        "1": {"x": 0, "y": 535},
                        "2": {"x": 0, "y": 117},
                        "3": {"x": 2, "y": 0},
                        "4": {"x": 3, "y": 117},
                        "5": {"x": 2, "y": 140},
                        "6": {"x": 2, "y": 0},
                        "7": {"x": 2, "y": 0},
                    },
                    "purchases": [
                        {"title": "YouTube Premium", "amount": 36},
                        {"title": "iCloud", "amount": 45},
                        {"title": "Notability", "amount": 70},
                        {"title": "Github Copilot", "amount": 38.34},
                        {"title": "Azure REGA", "amount": 31.32},
                        {"title": "Heroku Subscription", "amount": 25.22},
                    ],
                },
                {
                    "color": "blue",
                    "title": "🛒 Groceries",
                    "height": 316,
                    "columns": {
                        "1": {"x": 0, "y": 744},
                        "2": {"x": 1, "y": 418},
                        "3": {"x": 1, "y": 0},
                        "4": {"x": 2, "y": 0},
                        "5": {"x": 1, "y": 0},
                        "6": {"x": 3, "y": 0},
                        "7": {"x": 3, "y": 0},
                    },
                    "purchases": [
                        {"title": "كاتشب و صوصات من امازون", "amount": 152.87},
                        {"title": "مقاضي من كارفور", "amount": 123.32},
                        {"title": "مقاضي من لولو", "amount": 240.65},
                        {"title": "مقاضي من العثيم", "amount": 78.83},
                        {"title": "مقاضي من لولو يوم الجمعة", "amount": 161.5},
                        {"title": "منظفات للبيت", "amount": 39},
                        {"title": "مقاضي من زاوية الياسمين", "amount": 173},
                        {"title": "مويه المنهل دفتر", "amount": 222},
                    ],
                },
                {
                    "color": "blue",
                    "title": "🍔 Resturants & Cafes",
                    "height": 511,
                    "columns": {
                        "1": {"x": 0, "y": 999},
                        "2": {"x": 0, "y": 326},
                        "3": {"x": 0, "y": 0},
                        "4": {"x": 0, "y": 0},
                        "5": {"x": 0, "y": 0},
                        "6": {"x": 4, "y": 0},
                        "7": {"x": 4, "y": 0},
                    },
                    "purchases": [
                        {"title": "Calo Subscription", "amount": 1411},
                        {"title": "عصيرات الضاحية", "amount": 13},
                        {"title": "قهوة و كروسان من ايزي بيكري", "amount": 63},
                        {"title": "عشاء من سكشن بي هنقرستيشن", "amount": 58},
                        {"title": "CORE COFFEE", "amount": 18},
                        {"title": "Cheesecake factory", "amount": 162},
                        {"title": "قيف مي فايف مع الشباب", "amount": 81},
                        {"title": "كودو من جاهز", "amount": 35},
                        {"title": "تسعة اعشار الدوام", "amount": 15},
                        {"title": "عصير كوكتيل", "amount": 27},
                        {"title": "قهوة اليوم من بريهانت", "amount": 12},
                        {"title": "حلويات من بقالة الدوام", "amount": 7},
                        {"title": "عشاء فول و مطبق", "amount": 20},
                    ],
                },
                {
                    "color": "blue",
                    "title": "🗃 Others",
                    "height": 298,
                    "columns": {
                        "1": {"x": 0, "y": 117},
                        "2": {"x": 1, "y": 0},
                        "3": {"x": 1, "y": 316},
                        "4": {"x": 1, "y": 140},
                        "5": {"x": 3, "y": 117},
                        "6": {"x": 0, "y": 117},
                        "7": {"x": None, "y": None},
                    },
                    "purchases": [
                        {"title": "تأمين سيارتي", "amount": 1232},
                        {"title": "under armor", "amount": 314},
                        {"title": "كتاب من معرض الكتاب", "amount": 147.25},
                        {"title": "حلاق", "amount": 20},
                        {"title": "تصوير", "amount": 26},
                        {"title": "بخاخ الربو", "amount": 15.64},
                        {"title": "كڤر لجوالي", "amount": 207.39},
                        {"title": "حلاق", "amount": 60},
                        {"title": "مدخنة لحم", "amount": 216},
                    ],
                },
                {
                    "color": "blue",
                    "title": "",
                    "height": 1,
                    "columns": {
                        "1": {"x": 0, "y": 6},
                        "2": {"x": 0, "y": 3},
                        "3": {"x": 0, "y": 2},
                        "4": {"x": 2, "y": 1},
                        "5": {"x": 1, "y": 1},
                        "6": {"x": 0, "y": 1},
                        "7": {"x": None, "y": None},
                    },
                    "purchases": [{"title": None, "amount": None}],
                },
            ],
            "single_payments": [
                {"title": "Rent", "amount": 3500},
                {"title": "Car Loan", "amount": 2541},
                {"title": "Family Support", "amount": 2251},
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
    budget.last_updated = datetime.utcnow()
    session.commit()

    return budget_breakdown
