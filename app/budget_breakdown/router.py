# create router
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import validate_token_and_get_user
from app.infra.db import db_session
from .models import User

from .schemas import BudgetBreakdownJson
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
