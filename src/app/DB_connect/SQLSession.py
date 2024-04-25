from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class SQLSession:
    def __init__(self, db_url):
        self.sessionMaker = sessionmaker(bind=create_engine(db_url))

    # 创建数据库会话上下文管理器，实现数据库查询会话的自动创建和关闭
    @contextmanager
    def create_session(self):
        session = self.sessionMaker()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()