from sqlalchemy import Column, Integer, String, DateTime, Text
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
def update_relapse_sessions(user_id: int, relapse_sessions: list):
    session = SessionLocal()
    try:
        for relapse in relapse_sessions:
            # Преобразуем строку в объект datetime
            timestamp = relapse.get("date_time")
            if isinstance(timestamp, str):
                timestamp = datetime.strptime(timestamp, "%d.%m.%Y %H:%M")

            new_session = RelapseSession(
                user_id=user_id,
                current_step=relapse.get("current_step"),
                situation=relapse.get("situation"),
                thoughts=relapse.get("thoughts"),
                emotion_type=relapse.get("emotion_type"),
                emotion_score=relapse.get("emotion_score"),
                physical=relapse.get("physical"),
                behavior=relapse.get("behavior"),
                timestamp=timestamp or datetime.now(timezone.utc),
            )
            session.add(new_session)
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


def update_last_relapse_session(user_id: int, relapse_session: RelapseSession):
    session = SessionLocal()
    try:
        # Получаем последнюю сессию пользователя
        last_session = (
            session.query(RelapseSession)
            .filter(RelapseSession.user_id == user_id)
            .order_by(RelapseSession.timestamp.desc())
            .first()
        )
        if last_session:
            # Обновляем атрибуты сессии напрямую
            last_session.current_step = relapse_session.current_step
            last_session.situation = relapse_session.situation
            last_session.thoughts = relapse_session.thoughts
            last_session.emotion_type = relapse_session.emotion_type
            last_session.emotion_score = relapse_session.emotion_score
            last_session.physical = relapse_session.physical
            last_session.behavior = relapse_session.behavior

            # Если передана строковая дата, преобразуем ее в объект datetime
            timestamp = relapse_session.timestamp
            if isinstance(timestamp, str):
                timestamp = datetime.strptime(timestamp, "%d.%m.%Y %H:%M")

            last_session.timestamp = timestamp or datetime.now(timezone.utc)

            session.commit()
    finally:
        session.close()


def get_all_notes(user_id: int):
    session = SessionLocal()
    try:
        # Получаем все сессии рецидива для данного пользователя
        sessions = (
            session.query(RelapseSession)
            .filter(RelapseSession.user_id == user_id)
            .order_by(RelapseSession.timestamp.desc())
            .all()
        )

        if not sessions:
            return None

        # Формируем текст с заметками
        notes_text = ""
        for idx, session in enumerate(sessions, 1):
            notes_text += f"📄 *Заметка {idx}*\n"
            notes_text += f"🗓 *Дата*: {session.timestamp.strftime('%Y-%m-%d %H:%M') if session.timestamp else 'Не указана'}\n"
            notes_text += f"📍 *Ситуация*: {session.situation or 'Не указана'}\n"
            notes_text += f"💭 *Мысли*: {session.thoughts or 'Не указаны'}\n"
            notes_text += f"😶‍🌫️ *Эмоции*: {session.emotion_type or 'Не указаны'} (Оценка: {session.emotion_score or 'Не указана'})\n"
            notes_text += (
                f"💪 *Физическое состояние*: {session.physical or 'Не указано'}\n"
            )
            notes_text += f"🎯 *Поведение*: {session.behavior or 'Не указано'}\n"
            notes_text += f"{'-'*30}\n\n"

        return notes_text
    finally:
        session.close()
