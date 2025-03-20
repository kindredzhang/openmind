import logging
from contextvars import ContextVar
from peewee import *
from peewee import InterfaceError as PeeWeeInterfaceError

from peewee import PostgresqlDatabase
from playhouse.db_url import connect, parse
from playhouse.shortcuts import ReconnectMixin

class CustomReconnectMixin(ReconnectMixin):
    reconnect_errors = (
        # psycopg2
        (OperationalError, "termin"),
        (InterfaceError, "closed"),
        # peewee
        (PeeWeeInterfaceError, "closed"),
    )

class ReconnectingPostgresqlDatabase(CustomReconnectMixin, PostgresqlDatabase):
    pass

def register_connection(db_url):
    db = connect(db_url, unquote_password=True)
    if isinstance(db, PostgresqlDatabase):
        # Enable autoconnect for SQLite databases, managed by Peewee
        db.autoconnect = True
        db.reuse_if_open = True

        connection = parse(db_url, unquote_password=True)

        db = ReconnectingPostgresqlDatabase(**connection)
        db.connect(reuse_if_open=True)
    elif isinstance(db, SqliteDatabase):
        db.autoconnect = True
        db.reuse_if_open = True
    else:
        raise ValueError("Unsupported database connection")
    return db
