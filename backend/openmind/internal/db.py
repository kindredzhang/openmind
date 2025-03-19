from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import QueuePool, NullPool
from contextlib import contextmanager

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
)

Session = scoped_session(SessionLocal)


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


get_db = contextmanager(get_session)
