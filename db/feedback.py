from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime, timezone
from db.base import Base, SessionLocal


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, index=True)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))


def add_feedback(user_id: int, content: str):
    session = SessionLocal()
    try:
        feedback_entry = Feedback(
            user_id=user_id, content=content, timestamp=datetime.now(timezone.utc)
        )
        session.add(feedback_entry)
        session.commit()
        print(f"Feedback added for user {user_id}.")
    except Exception as e:
        session.rollback()
        print(f"Error adding feedback: {e}")
    finally:
        session.close()
