import os
from decouple import config

# from peewee import SqliteDatabase
from playhouse.pool import PooledSqliteExtDatabase  # , PooledPostgresqlExtDatabase


db_name = config("DATABASE_PATH", default="covid19_tracker.db")
path = os.getcwd().split("code")[0]
path = f"{path}code"

# db = SqliteDatabase(config('DATABASE_PATH', default='covid19_tracker.db'))
db = PooledSqliteExtDatabase(
    f"{path}/{db_name}",
    pragmas={
        "journal_mode": "wal",  # WAL-mode.
        "cache_size": -64 * 1000,  # 64MB cache.
        "foreign_keys": 1,
        "synchronous": 0,
    },
    max_connections=150,
    stale_timeout=3600,
    check_same_thread=False,
)

# Caso utilize-se do postgresql como banco de dados
# db = PooledPostgresqlExtDatabase(
#     config("DATABASE_PATH", default="covid19_tracker.db"),
#     max_connections=32,
#     stale_timeout=300,  # 5 minutes.
#     host='localhost',
#     user='username',
#     password='password')
