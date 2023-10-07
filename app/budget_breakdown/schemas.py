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
        class Columns(CamelModel):
            x: int | None = None
            y: int | None = None

        title: str
        purchases: list[Transaction]
        height: int | None = None
        # number of columns : {
        #   1: { x: 0, y: 0 },
        #   2: { x: 0, y: 0 },
        #   3: { x: 0, y: 0 },
        # }
        columns: dict[int, dict[str, int | None]] | None = None
        # TODO: Remove this
        x: int | None = None
        y: int | None = None

    # pydantic model
    money_in: list[Transaction]
    single_payments: list[Transaction]
    multi_payments: list[MultiPaymentBreakdown]
    last_month_money_remaining: float | None = None
    show_tour: bool | None = None
