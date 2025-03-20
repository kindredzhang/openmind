import json
import logging
from contextlib import contextmanager
from typing import Any, Optional

from openmind.env import (DATABASE_POOL_SIZE, DATABASE_SCHEMA, DATABASE_URL,
                          OPENMIND_DIR)
from openmind.internal.wrappers import register_connection
from peewee_migrate import Router
from sqlalchemy import Dialect, MetaData, create_engine, types
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import NullPool, QueuePool
from sqlalchemy.sql.type_api import _T
from typing_extensions import Self


class JSONField(types.TypeDecorator):
    impl = types.Text
    cache_ok = True

    def process_bind_param(self, value: Optional[_T], dialect: Dialect) -> Any:
        return json.dumps(value)

    def process_result_value(self, value: Optional[_T], dialect: Dialect) -> Any:
        if value is not None:
            return json.loads(value)

    def copy(self, **kw: Any) -> Self:
        return JSONField(self.impl.length)

    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        if value is not None:
            return json.loads(value)


# Workaround to handle the peewee migration
# This is required to ensure the peewee migration is handled before the alembic migration
def handle_peewee_migration(DATABASE_URL):
    # db = None
    try:
        # Replace the postgresql:// with postgres:// to handle the peewee migration
        print(DATABASE_URL)
        db = register_connection(DATABASE_URL.replace("postgresql://", "postgres://"))
        migrate_dir = OPENMIND_DIR / "internal" / "migrations"
        router = Router(db, logger=logging.getLogger("peewee_migrate"), migrate_dir=migrate_dir)
        router.run()
        db.close()

    except Exception as e:
        print(f"Failed to initialize the database connection: {e}")
        raise
    finally:
        # Properly closing the database connection
        if db and not db.is_closed():
            db.close()

        # Assert if db connection has been closed
        assert db.is_closed(), "Database connection is still open."


handle_peewee_migration("postgresql://postgres.afirrfctrbnucipmfybw:Kindredz155256-@aws-0-ap-northeast-1.pooler.supabase.com:5432/postgres")


SQLALCHEMY_DATABASE_URL = DATABASE_URL
print(SQLALCHEMY_DATABASE_URL)
if "sqlite" in SQLALCHEMY_DATABASE_URL:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    if DATABASE_POOL_SIZE > 0:
        engine = create_engine(
            SQLALCHEMY_DATABASE_URL,
            pool_size=DATABASE_POOL_SIZE,
            # max_overflow=DATABASE_POOL_MAX_OVERFLOW,
            # pool_timeout=DATABASE_POOL_TIMEOUT,
            # pool_recycle=DATABASE_POOL_RECYCLE,
            pool_pre_ping=True,
            poolclass=QueuePool,
        )
    else:
        engine = create_engine(
            SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, poolclass=NullPool
        )


SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
)
metadata_obj = MetaData(schema=DATABASE_SCHEMA)
Base = declarative_base(metadata=metadata_obj)
Session = scoped_session(SessionLocal)


def get_session():
    db = SessionLocal()
    print(db)
    try:
        yield db
    finally:
        db.close()


get_db = contextmanager(get_session)
