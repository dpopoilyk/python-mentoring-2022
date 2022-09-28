from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, asc, desc

from hometasks.contacts_api.core.db import ContactBase, Contact, ContactFields
from hometasks.contacts_api.core.decorators import handle_database_exceptions
from hometasks.contacts_api.core.entities import OrderDirection


class BaseRepository:
    _session: AsyncSession

    def __init__(self, session: AsyncSession):
        self._session = session


class ContactsRepository(BaseRepository):

    @handle_database_exceptions
    async def _commit_contact(self, contact: Contact):
        self._session.add(contact)
        await self._session.commit()
        await self._session.refresh(contact)

    @handle_database_exceptions
    async def create_contact(self, contact: ContactBase) -> Contact:
        contact = Contact(**contact.dict())
        await self._commit_contact(contact)
        return contact

    @handle_database_exceptions
    async def get_contacts(
            self,
            order_by: ContactFields = None,
            order_direction: OrderDirection = None,
            filters: dict = None,
            offset: int = None,
            limit: int = None
    ):
        query = select(Contact)
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
                query = query.where(getattr(Contact, field) == value)

        if offset is not None:
            query = query.offset(offset)

        if limit is not None:
            query = query.limit(limit)

        contacts = await self._session.execute(query)

        return [_[0] for _ in contacts.fetchall()]

    @handle_database_exceptions
    async def update_contact(self, contact: ContactBase, contact_to_update: Contact) -> tuple[Contact, list[str]]:
        updated_fields = []

        for key, value in contact.dict().items():
            current_value = getattr(contact_to_update, key)

            if current_value != value:
                setattr(contact_to_update, key, value)
                updated_fields.append(key)

        await self._commit_contact(contact_to_update)

        return contact_to_update, updated_fields

    @handle_database_exceptions
    async def delete_contact(self, contact: Contact):
        await self._session.delete(contact)
        await self._session.commit()
