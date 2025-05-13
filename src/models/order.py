from datetime import datetime, date
from typing import Optional, Annotated, Literal
from sqlmodel import Field, SQLModel, Column, DateTime
from pydantic import AfterValidator, model_validator, field_validator

class OrderBase(SQLModel):
    client_id: int = Field(ge=0)
    sale_id: int = Field(ge=0)
    batch_number: Optional[int] = Field(default=None, ge=0)
    sales_notes: Optional[str] = Field(default=None, max_length=255)
    notes: Optional[str] = Field(default=None, max_length=255)
    subtotal: float
    total: float
    discount_percentage: float = 0
    discount_amount: float = 0
    tax: float
    date: date
    location: Literal["Online Store", "Golf - experience"] = Field(max_length=255)

    @field_validator("date")
    @classmethod
    def validate_date(cls, value):
        if value > datetime.now().date():
            raise ValueError("date cannot be in the future")
        return value

class Order(OrderBase, table=True):
    __tablename__ = "orders"
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
    location: str
