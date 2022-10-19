from typing import Optional

from pydantic import BaseModel, Field


class ResponseMeta(BaseModel):
    fields: list[str] = None
    updated_fields: list[str] = None
    offset: int = None
    items_count: int = None

    def dict(self, *args, **kwargs):
        result = super(ResponseMeta, self).dict(*args, **kwargs)
        return {k: v for k, v in result.items() if v is not None}


class ResponseEntity(BaseModel):
    links: dict = {}
    data: list[dict]
    included: dict = None
    meta: ResponseMeta = None

    def __init__(self, **kwargs: any):
        super().__init__(**kwargs)

    def set_self_link(self, path):
        """
        need to call after initialization to add current link to response
        """
        self.add_link("self", path)

    def add_link(self, name, href):
        """
        add link to _links
        """
        self.links[name] = {"href": href}

    def dict(self, *args, **kwargs):
        """
        overwrite dict method to pop links and embedded fields if it is empty
        """

        result = super().dict(*args, **kwargs)

        if not result.get("links"):
            result.pop("links")

        if not result.get("included"):
            result.pop("included")

        if not result.get("meta"):
            result.pop("meta")

        return result


class ErrorResponse(BaseModel):
    class Error(BaseModel):
        title: str
        description: str

        field: str = None

        def dict(self, *args, **kwargs):
            result = super().dict(*args, **kwargs)

            if not result.get('field'):
                result.pop('field')

            return result

    title: str
    errors: Optional[list[Error]] = Field(default=None)
    detail: Optional[str] = Field(default=None)

    def dict(self, *args, **kwargs):
        result = super().dict(*args, **kwargs)

        if result.get('errors', None) is None:
            result.pop('errors')

        if result.get('detail', None) is None:
            result.pop('detail')

        return result

    class Config:
        schema_extra = {
            "example": {
                "title": "Some error title",
                "errors": [
                    {
                        "title": "Some error title",
                        "description": "some error description",
                    }
                ],
                "detail": "some error detail",
            }
        }