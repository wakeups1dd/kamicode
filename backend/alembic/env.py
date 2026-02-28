"""
KamiCode — Alembic Migration Environment

Supports both SQLite (sync engine, batch mode) and PostgreSQL (async engine).
Automatically selects based on the USE_SQLITE flag.
"""

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.core.config import get_settings
from app.models import Base  # noqa: F401 — ensures all models are imported

# ─── Alembic Config ────────────────────────────────────────────────
config = context.config
settings = get_settings()

# Override sqlalchemy.url with our env-based URL (sync version for Alembic)
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL_SYNC)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode — generates SQL without connecting."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # SQLite needs batch mode for schema changes
        render_as_batch=settings.USE_SQLITE,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        # SQLite needs batch mode
        render_as_batch=settings.USE_SQLITE,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in 'online' mode using an async host for PostgreSQL."""
    
    # We must construct the async engine using the ASYNC URL, not the sync URL from the main config
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = settings.DATABASE_URL
    
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Entry point for online migrations."""
    if settings.USE_SQLITE:
        # SQLite is sync, use standard create_engine
        connectable = create_engine(
            settings.DATABASE_URL_SYNC,
            poolclass=pool.NullPool,
        )
        with connectable.connect() as connection:
            do_run_migrations(connection)
        connectable.dispose()
    else:
        # PostgreSQL is async
        asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
