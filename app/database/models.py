import os
from dotenv import load_dotenv
from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

load_dotenv()

engine = create_async_engine(url=os.getenv("DB_URL"))
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, nullable=False)
    nickname: Mapped[str] = mapped_column(String(25), nullable=True)
    phone: Mapped[str] = mapped_column(String(15), nullable=True)


class PersonalParameter(Base):
    __tablename__ = "personal_parameters"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("users.id"))
    target: Mapped[bool] = mapped_column()  # True - набор веса, False - сброс веса
    activity: Mapped[float] = mapped_column()
    male: Mapped[bool] = mapped_column()  # True - мужчина, False - женщина
    age: Mapped[int] = mapped_column()
    growth: Mapped[int] = mapped_column()
    weight: Mapped[float] = mapped_column()


async def async_db_init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
