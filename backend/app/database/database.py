import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
from app.models import Base
from typing import Iterator
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()


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

    def __init__(self):
        """Initializes the Database."""
        try:
            driver = os.getenv("DATABASE_DRIVER")
            server = os.getenv("DATABASE_SERVER")
            db_name = os.getenv("DATABASE_NAME")
            username = os.getenv("DATABASE_USERNAME")
            password = os.getenv("DATABASE_PASSWORD")
            self.uri = f"{driver}://{username}:{password}@{server}/{db_name}"

            echo = os.getenv("DEVELOPMENT_MODE") == "True"
            self.engine = create_async_engine(
                self.uri,
                echo=echo,
                pool_size=5,
                max_overflow=10,
            )
            self.SessionLocal = sessionmaker(
                bind=self.engine, class_=AsyncSession, expire_on_commit=False
            )
        except ValueError as val_err:
            logging.error(f"Configuration error: {val_err}")
            raise
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

    async def get_session(self) -> Iterator[AsyncSession]:
        """Provides a context-managed async session for database operations.

        Yields:
            Iterator[AsyncSession]: The async session object for database interaction.

        Example:
            async with db.get_session() as session:
                # Perform database operations with the session
        """
        try:
            async with self.SessionLocal() as session:
                yield session
        except DBAPIError as db_err:
            # Handle database connection issues
            logging.error(f"Database connection error in session: {db_err}")
            raise
        except SQLAlchemyError as sql_err:
            # Handle SQLAlchemy related issues
            logging.error(f"SQLAlchemy error in session: {sql_err}")
            raise
        except Exception as e:
            # Handle other unexpected issues
            logging.error(f"Unexpected error in session: {e}")
            raise


# Creating a Database instance
db = Database()
