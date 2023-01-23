from enum import Enum

from pydantic import BaseModel

from hometasks.announcements_api.core.db import AnnouncementFields


class OrderDirection(Enum):
    DESC = "desc"
    ASC = "asc"


class QueryFilter(BaseModel):
    field: AnnouncementFields
    value: str
