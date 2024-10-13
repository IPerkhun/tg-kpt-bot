from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime, timezone
from db.base import Base, SessionLocal


class StopSmoking(Base):
    __tablename__ = "stop_smoking"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, index=True)
    stop_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    jobs = Column(Text, nullable=True)


# Получение данных отказа от курения для пользователя
def get_stop_smoking_data(user_id: int):
    session = SessionLocal()
    try:
        stop_data = (
            session.query(StopSmoking)
            .filter(StopSmoking.user_id == user_id)
            .order_by(StopSmoking.stop_time.desc())
            .first()
        )
        return stop_data
    finally:
        session.close()


# Обновление данных отказа от курения для пользователя
def update_stop_smoking_data(user_id: int, stop_smoking_data: dict):
    session = SessionLocal()
    try:
        stop_data = (
            session.query(StopSmoking)
            .filter(StopSmoking.user_id == user_id)
            .order_by(StopSmoking.stop_time.desc())
            .first()
        )
        if stop_data:
            stop_data.stop_time = datetime.strptime(
                stop_smoking_data["time"], "%Y-%m-%d %H:%M:%S"
            )
            stop_data.jobs = stop_smoking_data.get("jobs")
        else:
            # Если данных нет, создаем новую запись
            stop_data = StopSmoking(
                user_id=user_id,
                stop_time=datetime.strptime(
                    stop_smoking_data["time"], "%Y-%m-%d %H:%M:%S"
                ),
                jobs=stop_smoking_data.get("jobs"),
            )
            session.add(stop_data)
        session.commit()
    finally:
        session.close()
