from hometasks.contacts_api.core.db import get_session
from hometasks.contacts_api.core.repositories import ContactsRepository


def get_contacts_repository() -> ContactsRepository:
    return ContactsRepository(session=get_session())
