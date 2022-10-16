import typing
from enum import Enum

from pydantic import BaseModel

from hometasks.contacts_api.core.db import ContactFields


class OrderDirection(Enum):
    DESC = 'desc'
    ASC = 'asc'


class QueryFilter(BaseModel):
    field: ContactFields
    value: str
