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
            new_session = RelapseSession(
                user_id=user_id,
                current_step=relapse.get("current_step"),
                situation=relapse.get("situation"),
                thoughts=relapse.get("thoughts"),
                emotion_type=relapse.get("emotion_type"),
                emotion_score=relapse.get("emotion_score"),
                physical=relapse.get("physical"),
                behavior=relapse.get("behavior"),
                timestamp=relapse.get("date_time", datetime.now(timezone.utc)),
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
        return last_session if last_session else {"current_step": None}
    finally:
        session.close()


def update_last_relapse_session(user_id: int, relapse_session: dict):
    session = SessionLocal()
    try:
        last_session = (
            session.query(RelapseSession)
            .filter(RelapseSession.user_id == user_id)
            .order_by(RelapseSession.timestamp.desc())
            .first()
        )
        if last_session:
            last_session.current_step = relapse_session.get("current_step")
            last_session.situation = relapse_session.get("situation")
            last_session.thoughts = relapse_session.get("thoughts")
            last_session.emotion_type = relapse_session.get("emotion_type")
            last_session.emotion_score = relapse_session.get("emotion_score")
            last_session.physical = relapse_session.get("physical")
            last_session.behavior = relapse_session.get("behavior")
            last_session.timestamp = relapse_session.get(
                "date_time", datetime.now(timezone.utc)
            )
            session.commit()
    finally:
        session.close()
