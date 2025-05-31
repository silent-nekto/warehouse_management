from typing import List
from .models import Product, Order
from .repositories import ProductRepository, OrderRepository

class WarehouseService:
    def __init__(self, product_repo: ProductRepository, order_repo: OrderRepository):
        self.product_repo=product_repo
        self.order_repo=order_repo

    def create_product(self, name: str, quantity: int, price: float) -> Product:
        product=Product(id=None, name=name, quantity=quantity,price=price)
        self.product_repo.add(product)
        return product

    def change_product(self, product_id: int, quantity: int, price: float) -> None:
        self.product_repo.change(product_id, quantity, price)

    def create_order(self, products: List[Product]) -> Order:
        order=Order(id=None, products=products)
        self.order_repo.add(order)
        for p in products:
            self.change_product(p.id, p.quantity - 1, p.price)
        return order

    def complete_order(self, order_id: int):
        self.order_repo.delete(order_id)

    def cancel_order(self, order_id: int):
        order = self.order_repo.get(order_id)
        for p in order.products:
            self.change_product(p.id, p.quantity + 1, p.price)
        self.order_repo.delete(order_id)
