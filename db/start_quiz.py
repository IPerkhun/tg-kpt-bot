from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime, timezone
from db.base import Base, SessionLocal


class StartQuiz(Base):
    __tablename__ = "start_quizes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, index=True)
    smoking_type = Column(String(255), nullable=True)
    current_step = Column(String(255), nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))


# Получение последнего квиза для пользователя
def get_last_start_quiz(user_id: int):
    session = SessionLocal()
    try:
        last_quiz = (
            session.query(StartQuiz)
            .filter(StartQuiz.user_id == user_id)
            .order_by(StartQuiz.timestamp.desc())
            .first()
        )
        return last_quiz  # Вернем None, если квиз не найден
    finally:
        session.close()


# Обновление последнего квиза пользователя
def update_last_start_quiz(user_id, last_quiz: StartQuiz):
    session = SessionLocal()
    try:
        session.add(last_quiz)
        session.commit()
    finally:
        session.close()


# Добавление нового квиза
def add_new_start_quiz(user_id: int):
    session = SessionLocal()
    try:
        new_quiz = StartQuiz(
            user_id=user_id,
            current_step="step1",
            timestamp=datetime.now(timezone.utc),
        )
        session.add(new_quiz)
        session.commit()
        return new_quiz
    finally:
        session.close()
