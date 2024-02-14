from sqlalchemy import ForeignKey, String, BigInteger, Float, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from typing import List
import config

engine = create_async_engine(
    url=config.SQLALCHEMY_URL,
    echo=config.SQLALCHEMY_ECHO
)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


#Пример
class User(Base):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(String(), nullable=True)
    data: Mapped[dict] = mapped_column(JSON(), nullable=True)

    # cart_user: Mapped[List['Cart']] = relationship(back_populates='user_rel', cascade='all, delete')
    # order_rel: Mapped[List['Orders']] = relationship(back_populates='user_rel', cascade='all, delete')
    # collecting_rel: Mapped[List['Collecting_the_cake']] = relationship(back_populates='user_rel', cascade='all, delete')


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)