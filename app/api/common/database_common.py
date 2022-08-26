from sqlalchemy.orm import Session
from contextlib import contextmanager

from core.database import engine


class DBSessionContext(object):
    @contextmanager
    def get_session_scope(self):
        engine.dispose()
        session = Session(bind=engine, autocommit=False, autoflush=False)
        with session.begin():
            try:
                yield session
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()
