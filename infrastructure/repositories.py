from typing import List
from sqlalchemy.orm import Session
from domain.models import Order, Product
from domain.repositories import ProductRepository, OrderRepository
from .orm import ProductORM, OrderORM
from sqlalchemy.exc import NoResultFound
from domain.exceptions import OrderNotFound

class SqlAlchemyProductRepository(ProductRepository):
    def __init__(self, session: Session):
        self.session=session

    def add(self, product:Product):
        product_orm = ProductORM(
            name=product.name,
            quantity=product.quantity,
            price=product.price,
        )
        self.session.add(product_orm)
        self.session.flush()
        product.id = product_orm.id

    def get(self, product_id: int)->Product:
        product_orm = self.session.query(ProductORM).filter_by(id=product_id).one()
        return Product(
            id=product_orm.id,
            name=product_orm.name,
            quantity=product_orm.quantity,
            price=product_orm.price
        )

    def change(self, product_id: int, quantity: int, price: float)->None:
        product_orm = self.session.query(ProductORM).filter_by(id=product_id).one()
        product_orm.quantity = quantity
        product_orm.price = price
        self.session.add(product_orm)
        self.session.flush()

    def list(self) -> List[Product]:
        products_orm= self.session.query(ProductORM).all()
        return [
            Product(id=p.id, name=p.name, quantity=p.quantity, price=p.price)
            for p in products_orm
        ]

class SqlAlchemyOrderRepository(OrderRepository):
    def __init__(self, session: Session):
        self.session=session

    def add(self, order:Order):
        order_orm = OrderORM()
        order_orm.products = [
            self.session.query(ProductORM).filter_by(id=p.id).one()
            for p in order.products
        ]
        self.session.add(order_orm)
        self.session.flush()
        order.id = order_orm.id

    def delete(self, order_id: int):
        try:
            order_orm = self.session.query(OrderORM).filter_by(id=order_id).one()
        except NoResultFound:
            raise OrderNotFound(f'Order {order_id} was not found')
        self.session.delete(order_orm)
        self.session.flush()

    def get(self, order_id: int)->Order:
        try:
            order_orm = self.session.query(OrderORM).filter_by(id=order_id).one()
        except NoResultFound:
            raise OrderNotFound(f'Order {order_id} was not found')
        products = [
            Product(id=p.id, name=p.name, quantity=p.quantity, price=p.price)
            for p in order_orm.products
        ]
        return Order(id=order_orm.id, products=products)

    def list(self) -> List[Order]:
        orders_orm= self.session.query(OrderORM).all()
        orders=[]
        for order_orm in orders_orm:
            products = [
                Product(id=p.id, name=p.name, quantity=p.quantity, price=p.price)
                for p in order_orm.products
            ]
            orders.append(Order(id=order_orm.id, products=products))
        return orders
