import os

from enum import Enum
from datetime import date

from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Field

from hometasks.announcements_api.core.utils import generate_uid


DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_session = None


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


def get_session() -> AsyncSession:
    global async_session
    if async_session is None:
        async_session = sessionmaker(
            engine, class_=AsyncSession
        )
        async_session = async_session()
    return async_session


class AnnouncementBase(SQLModel):
    title: str
    body: str
    create_date: date


class Announcement(AnnouncementBase, table=True):
    __table_args__ = (UniqueConstraint("uid"),)

    uid: str = Field(default_factory=generate_uid, primary_key=True)


class AnnouncementFields(Enum):
    title = 'title'
    body = 'body'
    create_date = 'create_date'
