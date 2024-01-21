import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, DBAPIError, OperationalError
from app.models import Base
from typing import Iterator
from dotenv import load_dotenv
from pydantic import BaseSettings, ValidationError
import random
import logging

# Load environment variables from .env file
load_dotenv()


class DatabaseConfig(BaseSettings):
    database_driver: str
    database_server: str
    database_name: str
    database_username: str
    database_password: str
    development_mode: bool = False
    pool_size: int = 5
    max_overflow: int = 10
    pool_recycle: int = 3600
    pool_timeout: int = 30

    class Config:
        env_prefix = "DATABASE_"


class Database:
    """Handles database connections and session creation.

    This class is responsible for creating the database engine, initializing the database,
    and providing database sessions. It uses SQLAlchemy's async capabilities for
    asynchronous database interaction.

    Attributes:
        uri (str): The database connection URI.
        engine (AsyncEngine): The SQLAlchemy async engine for database connections.
        SessionLocal (sessionmaker): A sessionmaker instance configured for AsyncSession.
    """

    def __init__(self, config: DatabaseConfig):
        """Initializes the Database."""
        try:
            self.uri = f"{config.database_driver}://{config.database_username}:{config.database_password}@{config.database_server}/{config.database_name}"
            self.engine = create_async_engine(
                self.uri,
                echo=config.development_mode,
                pool_size=config.pool_size,
                max_overflow=config.max_overflow,
                pool_recycle=config.pool_recycle,
                pool_timeout=config.pool_timeout,
            )
            self.SessionLocal = sessionmaker(
                bind=self.engine, class_=AsyncSession, expire_on_commit=False
            )
        except Exception as e:
            logging.error(f"Error initializing database engine: {e}")
            raise

    async def init_db(self) -> None:
        """Initializes the database by creating tables based on the models.

        This method should be run to create the database tables before the application starts.
        It should be used carefully, especially when connecting to a production database.
        """
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
        except DBAPIError as db_err:
            # Handle database connection issues
            logging.error(f"Database connection error during initialization: {db_err}")
            raise
        except SQLAlchemyError as sql_err:
            # Handle SQLAlchemy related issues
            logging.error(f"SQLAlchemy error during database initialization: {sql_err}")
            raise
        except Exception as e:
            # Handle other unexpected issues
            logging.error(f"Unexpected error during database initialization: {e}")
            raise

    async def _execute_with_retry(
        self, operation, max_retries=3, initial_delay=1, backoff_factor=2
    ):
        """Executes a database operation with exponential backoff retries.

        Args:
            operation: The asynchronous database operation to perform.
            max_retries (int): Maximum number of retries.
            initial_delay (int): Initial delay between retries in seconds.
            backoff_factor (int): Factor by which to multiply the delay for each retry.

        Returns:
            The result of the operation, if successful.

        Raises:
            Exception: If the operation fails after the maximum retries.
        """
        attempt = 0
        delay = initial_delay
        while attempt < max_retries:
            try:
                return await operation()
            except OperationalError as e:
                attempt += 1
                logging.warning(
                    f"Database operation failed, attempt {attempt}/{max_retries}: {e}"
                )
                if attempt >= max_retries:
                    raise
                await asyncio.sleep(delay)
                delay *= backoff_factor + random.uniform(0, 0.1)  # Adding jitter

    async def get_session(self) -> Iterator[AsyncSession]:
        """Provides a context-managed async session for database operations.

        Yields:
            Iterator[AsyncSession]: The async session object for database interaction.

        Example:
            async with db.get_session() as session:
                # Perform database operations with the session
        """

        async def create_session():
            async with self.SessionLocal() as session:
                yield session

        return await self._execute_with_retry(create_session)


# Read and validate configuration
try:
    config = DatabaseConfig()
except ValidationError as e:
    logging.error(f"Configuration validation error: {e}")
    raise

# Creating a Database instance
db = Database()
