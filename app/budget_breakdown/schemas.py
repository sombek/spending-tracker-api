from humps import camel
from pydantic import BaseModel, ConfigDict, field_validator, validator


def to_camel(string):
    return camel.case(string)


class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True


class Transaction(CamelModel):
    title: str | None = None
    amount: float | None = None


class BudgetBreakdownJson(CamelModel):
    class MultiPaymentBreakdown(CamelModel):
        title: str
        purchases: list[Transaction]
        height: int | None = None
        x: int | None = None
        y: int | None = None

    # pydantic model
    money_in: list[Transaction]
    single_payments: list[Transaction]
    multi_payments: list[MultiPaymentBreakdown]
