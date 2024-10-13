from sqlalchemy import Column, Integer, String, DateTime, Text
from typing import List
from datetime import datetime, timezone
from db.base import Base, SessionLocal


class RelapseSession(Base):
    __tablename__ = "relapse_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, index=True)
    current_step = Column(String(255), nullable=True)
    situation = Column(String(255), nullable=True)
    thoughts = Column(Text, nullable=True)
    emotion_type = Column(String(50), nullable=True)
    emotion_score = Column(Integer, nullable=True)
    physical = Column(Text, nullable=True)
    behavior = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))


def get_relapse_sessions(user_id: int):
    session = SessionLocal()
    try:
        sessions = (
            session.query(RelapseSession)
            .filter(RelapseSession.user_id == user_id)
            .all()
        )
        return sessions
    finally:
        session.close()


# Функция для обновления списка сессий рецидива пользователя
def add_new_relapse_session(user_id: int, relapse_session: dict):
    session = SessionLocal()
    try:
        relapse_session = RelapseSession(
            user_id=user_id,
            timestamp=relapse_session.get("date_time", datetime.now(timezone.utc)),
        )
        session.add(relapse_session)
        session.commit()
    finally:
        session.close()


def get_last_relapse_session(user_id: int):
    session = SessionLocal()
    try:
        last_session = (
            session.query(RelapseSession)
            .filter(RelapseSession.user_id == user_id)
            .order_by(RelapseSession.timestamp.desc())
            .first()
        )
        return last_session
    finally:
        session.close()


# Обновление последней сессии рецидива пользователя
def update_last_relapse_session(user_id: int, relapse_session: RelapseSession):
    session = SessionLocal()
    try:
        relapse_session.user_id = user_id
        session.add(relapse_session)
        session.commit()
    finally:
        session.close()


def get_all_notes(user_id: int):
    sess = SessionLocal()
    try:
        # Получаем все сессии рецидива для данного пользователя
        sessions = (
            sess.query(RelapseSession)
            .filter(RelapseSession.user_id == user_id)
            .order_by(RelapseSession.timestamp.desc())
            .all()
        )

        if not sessions:
            return None

        # Формируем текст с заметками
        notes_text = ""
        for idx, s in enumerate(sessions, 1):
            notes_text += f"📄 *Заметка {idx}*\n"
            notes_text += f"🗓 *Дата*: {s.timestamp.strftime('%Y-%m-%d %H:%M') if s.timestamp else 'Не указана'}\n"
            notes_text += f"📍 *Ситуация*: {s.situation or 'Не указана'}\n"
            notes_text += f"💭 *Мысли*: {s.thoughts or 'Не указаны'}\n"
            notes_text += f"😶‍🌫️ *Эмоции*: {s.emotion_type or 'Не указаны'} (Оценка: {s.emotion_score or 'Не указана'})\n"
            notes_text += f"💪 *Физическое состояние*: {s.physical or 'Не указано'}\n"
            notes_text += f"🎯 *Поведение*: {s.behavior or 'Не указано'}\n"
            notes_text += f"{'-'*30}\n\n"

        return notes_text
    finally:
        sess.close()
