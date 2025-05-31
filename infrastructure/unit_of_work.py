from domain.unit_of_work import UnitOfWork

class SqlAlchemyUnitOfWork(UnitOfWork):

    def __init__(self, session):
        self._session = session

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if not exception_type:
            self.commit()

    def commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()
