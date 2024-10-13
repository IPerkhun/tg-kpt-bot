import os
import logging
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)

# Подключение к базе данных
DATABASE_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)
logging.info(f"Connecting to the database at {DATABASE_URL}")
engine = create_engine(
    DATABASE_URL, echo=False
)  # echo=False для отключения логирования SQL-запросов
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Определение базового класса для моделей
Base = declarative_base()


# Модель для таблицы сообщений
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, index=True)
    message_type = Column(String(50))  # Тип сообщения (например, "text" или "voice")
    content = Column(Text)  # Содержимое сообщения
    timestamp = Column(DateTime, default=datetime.utcnow)  # Время отправки сообщения
    role = Column(String(10))  # Роль отправителя (например, "user" или "bot")


# Функция для создания таблиц в базе данных
def create_tables():
    Base.metadata.create_all(bind=engine)


# Функция для проверки подключения к базе данных
def test_db_connection():
    session = SessionLocal()
    try:
        session.execute("SELECT 1")  # Простой запрос для проверки соединения
        logging.info("Database connection successful.")
    except Exception as e:
        logging.error(f"Error connecting to the database: {e}")
        raise
    finally:
        session.close()


# Функция для получения сессии базы данных
def get_db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# Функция для добавления сообщения в базу данных
def add_user_message(user_id: int, message_data: dict):
    session = SessionLocal()
    try:
        new_message = Message(
            user_id=user_id,
            message_type=message_data["type"],
            content=message_data["content"],
            timestamp=datetime.utcnow(),  # Всегда используем UTC
            role=message_data["role"],
        )
        session.add(new_message)
        session.commit()
        logging.info(f"Message added for user {user_id}.")
    except Exception as e:
        session.rollback()
        logging.error(f"Error adding message: {e}")
    finally:
        session.close()


# Функция для получения всех сообщений пользователя
def get_user_messages(user_id: int):
    session = SessionLocal()
    try:
        messages = session.query(Message).filter(Message.user_id == user_id).all()
        return messages
    finally:
        session.close()
