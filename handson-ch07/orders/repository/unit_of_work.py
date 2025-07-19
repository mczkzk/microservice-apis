from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class UnitOfWork:

    def __init__(self):
        self.session_maker = sessionmaker(bind=create_engine("sqlite:///orders.db"))

    # コンテキストマネージャーのエントリーポイント
    def __enter__(self):
        self.session = self.session_maker()
        return self

    # コンテキストマネージャーの終了ポイント
    def __exit__(self, exc_type, exc_val, traceback):
        # exc_type: 例外の型
        # exc_val: 例外の値
        # traceback: 例外のトレースバック
        if exc_type is not None:
            self.rollback()
            self.session.close()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
