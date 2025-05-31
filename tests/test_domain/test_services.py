import pytest
from typing import List, Dict
from domain.repositories import OrderRepository, ProductRepository
from domain.models import Product, Order
from domain.services import WarehouseService
from domain.exceptions import OrderNotFound, ProductNotFound


class MockProductRepository(ProductRepository):
    def __init__(self):
        self._repo: Dict[int, Product] = {}
        self._id = 1

    def add(self, product: Product):
        self._repo[self._id] = product
        product.id = self._id
        self._id += 1

    def change(self, product_id: int, quantity: int, price: float):
        if product_id not in self._repo:
            raise ProductNotFound
        self._repo[product_id].quantity = quantity
        self._repo[product_id].price = price

    def get(self, product_id: int) -> Product:
        if product_id not in self._repo:
            raise ProductNotFound
        return self._repo[product_id]

    def list(self) -> List[Product]:
        return [v for v in self._repo.values()]


class MockOrderRepository(OrderRepository):
    def __init__(self):
        self._repo: Dict[int, Order] = {}
        self._id = 1

    def add(self, order: Order):
        self._repo[self._id] = order
        order.id = self._id
        self._id += 1

    def get(self, order_id: int) -> Order:
        if order_id not in self._repo:
            raise OrderNotFound
        return self._repo[order_id]

    def delete(self, order_id: int):
        if order_id not in self._repo:
            raise OrderNotFound
        self._repo.pop(order_id)

    def list(self) -> List[Order]:
        return [v for v in self._repo.values()]


@pytest.fixture
def order_repo():
    yield MockOrderRepository()


@pytest.fixture
def product_repo():
    yield MockProductRepository()


class TestServices:
    def test_create_product(self, product_repo, order_repo):
        svc = WarehouseService(product_repo, order_repo)
        p = svc.create_product(name='test_product', quantity=100, price=100)
        assert isinstance(p.id, int)
        assert p.name == 'test_product'
        assert p.quantity == 100
        assert p.price == 100

    def test_change_product_quantity(self, product_repo, order_repo):
        svc = WarehouseService(product_repo, order_repo)
        p = svc.create_product(name='test_product', quantity=100, price=100)
        svc.change_product(p.id, quantity=50, price=200)
        assert p.quantity == 50
        assert p.price == 200

    def test_create_order(self, product_repo, order_repo):
        svc = WarehouseService(product_repo, order_repo)
        p = svc.create_product(name='test_product', quantity=100, price=100)
        o = svc.create_order([p])
        assert isinstance(o.id, int)
        assert o.products[0] is p
        assert p.quantity == 99

    def test_complete_order(self, product_repo, order_repo):
        svc = WarehouseService(product_repo, order_repo)
        p = svc.create_product(name='test_product', quantity=100, price=100)
        o = svc.create_order([p])
        svc.complete_order(o.id)
        with pytest.raises(OrderNotFound):
            order_repo.get(o.id)

    def test_cancel_order(self, product_repo, order_repo):
        svc = WarehouseService(product_repo, order_repo)
        p = svc.create_product(name='test_product', quantity=100, price=100)
        o = svc.create_order([p])
        svc.cancel_order(o.id)
        with pytest.raises(OrderNotFound):
            order_repo.get(o.id)
        p = product_repo.get(p.id)
        assert p.quantity == 100
