from datetime import date

from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, asc, desc, Date

from hometasks.announcements_api.core.db import AnnouncementBase, Announcement, AnnouncementFields
from hometasks.announcements_api.core.decorators import handle_database_exceptions
from hometasks.announcements_api.core.entities import OrderDirection
from hometasks.announcements_api.core.exceptions import DatabaseException


class BaseRepository:
    _session: AsyncSession

    def __init__(self, session: AsyncSession):
        self._session = session


class AnnouncementsRepository(BaseRepository):

    @handle_database_exceptions
    async def _commit_announcement(self, contact: Announcement):
        self._session.add(contact)
        await self._session.commit()
        await self._session.refresh(contact)

    @handle_database_exceptions
    async def create_announcement(self, announcement: AnnouncementBase) -> Announcement:
        announcement = Announcement(**announcement.dict())
        await self._commit_announcement(announcement)
        return announcement

    @handle_database_exceptions
    async def get_announcements(
            self,
            order_by: AnnouncementFields = None,
            order_direction: OrderDirection = None,
            filters: dict = None,
            offset: int = None,
            limit: int = None
    ):
        query = select(Announcement)
        if order_by is not None:
            value = order_by.value

            if order_direction is not None:
                match order_direction:
                    case OrderDirection.ASC:
                        value = asc(value)
                    case OrderDirection.DESC:
                        value = desc(value)

            query = query.order_by(value)

        if filters is not None:
            for field, value in filters.items():
                if type(getattr(Announcement, field).type) is Date:
                    try:
                        value = date.fromisoformat(value)
                    except ValueError as err:
                        raise DatabaseException(err)
                query = query.where(getattr(Announcement, field) == value)

        if offset is not None:
            query = query.offset(offset)

        if limit is not None:
            query = query.limit(limit)

        announcements = await self._session.execute(query)

        return [_[0] for _ in announcements.fetchall()]

    @handle_database_exceptions
    async def update_announcement(self, announcement: AnnouncementBase, announcement_to_update: Announcement) -> tuple[Announcement, list[str]]:
        updated_fields = []
        not_updatable = (AnnouncementFields.create_date.value, )

        for key, value in announcement.dict(exclude_unset=True).items():
            if key in not_updatable:
                raise DatabaseException(f'Field [{key}] is not updatable.')
            current_value = getattr(announcement_to_update, key)

            if current_value != value:
                setattr(announcement_to_update, key, value)
                updated_fields.append(key)

        await self._commit_announcement(announcement_to_update)

        return announcement_to_update, updated_fields

    @handle_database_exceptions
    async def delete_announcement(self, contact: Announcement):
        await self._session.delete(contact)
        await self._session.commit()
