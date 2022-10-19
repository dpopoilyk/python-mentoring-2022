from hometasks.announcements_api.core.db import get_session
from hometasks.announcements_api.core.repositories import AnnouncementsRepository


def get_announcements_repository() -> AnnouncementsRepository:
    return AnnouncementsRepository(session=get_session())
