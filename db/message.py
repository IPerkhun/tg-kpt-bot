from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime, timezone
from db.base import Base, SessionLocal


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, index=True)
    message_type = Column(String(50))
    content = Column(Text)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    role = Column(String(10))


def add_user_message(user_id: int, message_data: dict):
    session = SessionLocal()
    try:
        new_message = Message(
            user_id=user_id,
            message_type=message_data["type"],
            content=message_data["content"],
            timestamp=message_data.get("timestamp", datetime.now(timezone.utc)),
            role=message_data["role"],
        )
        session.add(new_message)
        session.commit()
        print(f"Message added for user {user_id}.")
    except Exception as e:
        session.rollback()
        print(f"Error adding message: {e}")
    finally:
        session.close()


def get_user_messages(user_id: int):
    session = SessionLocal()
    try:
        messages = session.query(Message).filter(Message.user_id == user_id).all()
        return messages
    finally:
        session.close()


def get_last_n_messages(user_id: int, n: int = 6):
    session = SessionLocal()
    try:
        messages = (
            session.query(Message)
            .filter(Message.user_id == user_id)
            .order_by(Message.timestamp.desc())
            .limit(n)
            .all()
        )
        return messages[::-1]
    finally:
        session.close()
