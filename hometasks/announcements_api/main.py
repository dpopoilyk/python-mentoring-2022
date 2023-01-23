from typing import Optional

from fastapi import FastAPI, Depends, Query, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, create_model

from hometasks.announcements_api.core.db import (
    AnnouncementBase,
    AnnouncementFields,
)
from hometasks.announcements_api.core.decorators import handle_endpoint_errors
from hometasks.announcements_api.core.entities import OrderDirection
from hometasks.announcements_api.core.exceptions import NotFoundException
from hometasks.announcements_api.core.repositories import \
    AnnouncementsRepository
from hometasks.announcements_api.core.depends import \
    get_announcements_repository
from hometasks.announcements_api.core.responses import \
    ResponseEntity, ResponseMeta

app = FastAPI()


@app.get("/status", description="test")
async def root():
    return JSONResponse({"status": "OK"})


@app.post("/announcements", description="create announcement")
@handle_endpoint_errors
async def create_announcement(
    announcement: AnnouncementBase,
    request: Request,
    repository: AnnouncementsRepository = Depends(
        get_announcements_repository
    ),
):
    announcement = await repository.create_announcement(announcement)

    response = ResponseEntity(
        data=((contact_dict := announcement.dict()),),
        meta=ResponseMeta(fields=list(contact_dict.keys()), items_count=1),
    )
    response.set_self_link(request.url.path)
    return JSONResponse(jsonable_encoder(response), 201)


@app.get("/announcements", description="get announcements")
@handle_endpoint_errors
async def get_contacts(
    request: Request,
    repository: AnnouncementsRepository = Depends(
        get_announcements_repository
    ),
    order_by: Optional[AnnouncementFields] = Query(
        AnnouncementFields.create_date
    ),
    order_direction: Optional[OrderDirection] = Query(OrderDirection.ASC),
    filters: BaseModel = Depends(
        create_model(
            "Filters",
            **{
                field.value: (Optional[str], None)
                for field in AnnouncementFields
            },
        )
    ),
    limit: int = Query(5),
    offset: int = Query(0),
):
    announcements = await repository.get_announcements(
        order_by,
        order_direction,
        {k: v for k, v in filters.dict().items() if v is not None},
        offset,
        limit,
    )

    response = ResponseEntity(
        data=(announcement.dict() for announcement in announcements),
        meta=ResponseMeta(
            fields=list(announcements[0].dict().keys())
            if len(announcements) > 0
            else None,
            items_count=len(announcements),
            offset=offset,
        ),
    )
    response.set_self_link(request.url.path)

    return JSONResponse(jsonable_encoder(response))


@app.put("/announcements/{uid}", description="update announcement")
@handle_endpoint_errors
async def update_announcement(
    uid: str,
    announcement: AnnouncementBase,
    request: Request,
    repository: AnnouncementsRepository = Depends(
        get_announcements_repository
    ),
):
    try:
        announcement_to_update = (
            await repository.get_announcements(filters={"uid": uid})
        )[0]
    except IndexError:
        raise NotFoundException(f'Announcement with uid: "{uid}" not found')

    announcement_to_update, updated_fields = \
        await repository.update_announcement(
            announcement, announcement_to_update
        )

    response = ResponseEntity(
        data=((updated_contact_dict := announcement_to_update.dict()),),
        meta=ResponseMeta(
            fields=list(updated_contact_dict.keys()),
            updated_fields=updated_fields,
            items_count=1,
        ),
    )
    response.set_self_link(request.url.path)

    return JSONResponse(jsonable_encoder(response))


@app.delete("/announcements/{uid}", description="delete announcement")
@handle_endpoint_errors
async def delete_announcement(
    uid: str,
    repository: AnnouncementsRepository = Depends(
        get_announcements_repository
    ),
):
    try:
        announcement_to_delete = (
            await repository.get_announcements(filters={"uid": uid})
        )[0]
    except IndexError:
        raise NotFoundException(f'Announcement with uid: "{uid}" not found')

    await repository.delete_announcement(announcement_to_delete)

    return Response(status_code=204)
