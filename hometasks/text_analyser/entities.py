from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class ResourcesTypes(Enum):
    FILE = "file"
    RESOURCE = "resource"


@dataclass
class ResourceMeta:
    type: ResourcesTypes
    name: str
    execution_date: datetime
