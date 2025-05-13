from datetime import datetime
from sqlmodel import Field, SQLModel
from typing import Optional

class ProductBase(SQLModel):
    name: str = Field(max_length=255)
    price: float = Field(ge=0)

class Product(ProductBase, table=True):
    __tablename__ = "products"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
