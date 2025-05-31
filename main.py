from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from domain.services import WarehouseService
from infrastructure.orm import Base
from infrastructure.repositories import SqlAlchemyProductRepository, SqlAlchemyOrderRepository
from infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from infrastructure.database import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionFactory=sessionmaker(bind=engine)
Base.metadata.create_all(engine)

def main():
    session = SessionFactory()
    product_repo = SqlAlchemyProductRepository(session)
    order_repo = SqlAlchemyOrderRepository(session)

    uow = SqlAlchemyUnitOfWork(session)

    warehouse_service = WarehouseService(product_repo, order_repo)
    # наполним базу продуктами
    with uow:
        warehouse_service.complete_order(666)
    # with uow:
    #     apple = warehouse_service.create_product(name="apple", quantity=10, price=100)
    #     microsoft = warehouse_service.create_product(name="microsoft", quantity=10, price=200)
    #     warehouse_service.change_product(apple.id, 666, 0.666)
    #     order = warehouse_service.create_order([apple, microsoft])
    #     warehouse_service.cancel_order(order.id)
        # uow.commit()
        # print(f"create product: {new_product}")
        # todo add some actions

if __name__ == "__main__":
    main()
