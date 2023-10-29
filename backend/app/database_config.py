import os
from contextlib import asynccontextmanager

from databases import Database
from dotenv import load_dotenv
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()


class DatabaseConfig:
    DB_ENGINE = os.getenv("DB_ENGINE")
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")

    @classmethod
    def generate_db_url(cls):
        """Generate the url for specific database"""
        return f"{cls.DB_ENGINE}://{cls.DB_USERNAME}:{cls.DB_PASSWORD}@{cls.DB_HOST}/{cls.DB_NAME}"


class DatabaseConnection:
    """
    Representation of custom ORM solution
    """

    metadata = MetaData()
    DATABASE_URL = DatabaseConfig.generate_db_url()

    engine = create_async_engine(DATABASE_URL, echo=True)
    AsyncSessionLocal = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    database = Database(DATABASE_URL)


@asynccontextmanager
async def db_session():
    """Provide a transactional scope around a series of operations."""
    async_session = DatabaseConnection.AsyncSessionLocal()
    try:
        yield async_session
        await async_session.commit()
    except Exception as e:
        await async_session.rollback()
        raise e
    finally:
        await async_session.close()
