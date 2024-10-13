import os
from sqlalchemy import create_engine

db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")
db_host = "db"  # Используем имя сервиса как хост
db_port = "5432"

engine = create_engine(
    f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)


def test_db_connection():
    with engine.connect() as connection:
        result = connection.execute("SELECT 1")
        assert result.scalar() == 1
        print("Connection successful")
