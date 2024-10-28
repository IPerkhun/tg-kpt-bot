import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values
import logging

env_values = dotenv_values(".env")

for key, value in env_values.items():
    os.environ[key] = value

DATABASE_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)
logging.info(f"Connecting to the database at {DATABASE_URL}")

engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def create_tables():
    logging.info("Creating tables in the database.")
    Base.metadata.create_all(bind=engine)


def get_db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_db_connection():
    session = SessionLocal()
    try:
        session.execute(text("SELECT 1"))
        print("Database connection successful.")
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise
    finally:
        session.close()
