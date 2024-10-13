# %%
from sqlalchemy import create_engine, Column, BigInteger, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from datetime import datetime, timezone


POSTGRES_USER = "kpt_bot_user"
POSTGRES_PASSWORD = "KJSNH2453thGHVSIUBVkfjsnjv"
POSTGRES_DB = "kpt_bot"

db_user = POSTGRES_USER
db_host = "164.92.186.76"
db_password = POSTGRES_PASSWORD
db_port = 5432
db_name = POSTGRES_DB

# Создаем базу моделей
Base = declarative_base()

engine = create_engine(
    f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)
Session = sessionmaker(bind=engine)
session = Session()


# Модель таблицы users
class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    deleted_at = Column(DateTime, nullable=True)


# Создаем таблицу в базе данных (если её нет)
Base.metadata.create_all(engine)

# Добавляем пользователя
# new_user = User(id=67306629)
# session.add(new_user)
# session.commit()

# Обновляем пользователя
user = session.query(User).filter_by(id=67306629).first()
user.deleted_at = datetime.now(timezone.utc)
session.commit()

# Закрываем сессию
session.close()

# Update user
user = session.query(User).filter_by(id=67306629).first()
user.deleted_at = None
session.commit()

# %%
