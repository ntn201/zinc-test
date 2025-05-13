from datetime import datetime
from sqlmodel import Field, SQLModel
from typing import Optional

class OrderItemBase(SQLModel):
    product_id: int = Field(ge=0)
    quantity: int = Field()
    order_id: int = Field(ge=0)

class OrderItem(OrderItemBase, table=True):
    __tablename__ = "order_items"
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id", index=True)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
