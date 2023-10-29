import asyncio

from app.database_config import DatabaseConnection
from app.db.attacks import Attack
from app.db.results import AttackResult
from app.db.website import URL, InputField, Website


async def create_tables():
    """The function which should be run during ``setup`` in order to create the initial tables in DB"""
    async with DatabaseConnection.engine.begin() as conn:
        await conn.run_sync(
            DatabaseConnection.metadata.create_all,
            tables=[
                Website.__table__,
                URL.__table__,
                InputField.__table__,  # website.py
                Attack.__table__,  # attack.py
                AttackResult.__table__,
            ],  # results.py
        )


if __name__ == "__main__":
    asyncio.run(create_tables())
