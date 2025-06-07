
import sys
import os
from logging.config import fileConfig

from sqlalchemy import pool
from alembic import context

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.models import SQLModel  # use o caminho correto
from database import DATABASE_URL

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata

def get_url():
    return DATABASE_URL

def run_migrations_offline():
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    from sqlalchemy import create_engine
    connectable = create_engine(get_url(), poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()