import csv
import datetime

from src.models.order import Order
from src.models.product import Product
from src.models.order_item import OrderItem

from sqlalchemy import select, text
from sqlmodel.ext.asyncio.session import AsyncSession

import logging 
logger = logging.getLogger(__name__)

DATA_FILE = "sales.csv"

class ImportSalesController:
    def __init__(self, session: AsyncSession):
        self.session = session

    @classmethod
    def parse_csv_row_to_dict(cls, row: list[str]) -> dict:
        return {
            "order_date": datetime.datetime.strptime(row[0], "%m/%d/%Y").date(),
            "client_id": int(row[1]),
            "sale_id": int(row[2]),
            "item_name": row[3],
            "batch_number": int(row[4]) if row[4] != "---" else None,
            "sales_notes": row[5],
            "location": row[6],
            "notes": row[7],
            # color row 8 but skip
            # size row 9 but skip
            "item_price": float(row[10]),
            "quantity": int(row[11]),
            "subtotal": float(row[12]),
            "discount_percentage": float(row[13]),
            "discount_amount": float(row[14]),
            "tax": float(row[15]),
            "item_total": float(row[16]),
            "total_paid": float(row[17]),
            "payment_method": row[18],
        }

    async def save_product(self, parsed_row: dict) -> Product:
        query = select(Product).where(Product.name == parsed_row["item_name"])
        result = await self.session.exec(query)
        product = result.scalar_one_or_none()

        if not product:
            product = Product(name=parsed_row["item_name"], price=parsed_row["item_price"])
            product = Product.model_validate(product)
            self.session.add(product)
            await self.session.commit()
        return product

    async def save_order(self, parsed_row: dict) -> Order:
        order = Order(
            client_id=parsed_row["client_id"],
            sale_id=parsed_row["sale_id"],
            batch_number=parsed_row["batch_number"],
            sales_notes=parsed_row["sales_notes"],
            notes=parsed_row["notes"],
            subtotal=parsed_row["subtotal"],
            total=parsed_row["item_total"],
            discount_percentage=parsed_row["discount_percentage"],
            discount_amount=parsed_row["discount_amount"],
            tax=parsed_row["tax"],
            date=parsed_row["order_date"],
            location=parsed_row["location"],
        )
        order = Order.model_validate(order)
        self.session.add(order)
        await self.session.commit()
        return order

    async def save_order_item(
        self,
        parsed_row: dict,
        product: Product,
        order: Order,
    ) -> OrderItem:
        # Ensure we have the latest state of product and order
        await self.session.refresh(product)
        await self.session.refresh(order)

        order_item = OrderItem(
            product_id=product.id,
            quantity=parsed_row["quantity"],
            order_id=order.id
        )
        order_item = OrderItem.model_validate(order_item)
        self.session.add(order_item)
        await self.session.commit()
        await self.session.refresh(order_item)
        return order_item

    async def truncate_tables(self):
        await self.session.exec(text("""TRUNCATE TABLE "orders" RESTART IDENTITY CASCADE"""))
        await self.session.exec(text("""TRUNCATE TABLE "order_items" RESTART IDENTITY CASCADE"""))
        await self.session.exec(text("""TRUNCATE TABLE "products" RESTART IDENTITY CASCADE"""))
        await self.session.commit()

    async def import_sales(self, truncate_tables: bool = False):
        imported_rows = 0
        if truncate_tables:
            await self.truncate_tables()
        with open(DATA_FILE, "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                try:
                    parsed_row = self.parse_csv_row_to_dict(row)
                    product = await self.save_product(parsed_row)
                    order = await self.save_order(parsed_row)
                    order_item = await self.save_order_item(parsed_row, product, order)
                    imported_rows += 1
                except Exception as e:
                    logger.exception(e)
                    continue
        return imported_rows
