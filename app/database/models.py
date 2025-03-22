from sqlalchemy import ForeignKey, String, BigInteger, Column, DateTime, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from datetime import datetime

from config import DB_URL

engine = create_async_engine(url=DB_URL,
                             echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    image = mapped_column(LargeBinary, nullable=False)
    created_at = mapped_column(DateTime, default=datetime.utcnow)
    promt = mapped_column(String, nullable=False)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


