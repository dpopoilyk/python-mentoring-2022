from typing import Optional

from fastapi import FastAPI, Depends, Query, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, create_model

from hometasks.contacts_api.core.db import ContactBase, ContactFields, init_db
from hometasks.contacts_api.core.decorators import handle_endpoint_errors
from hometasks.contacts_api.core.entities import OrderDirection, QueryFilter
from hometasks.contacts_api.core.exceptions import NotFoundException
from hometasks.contacts_api.core.repositories import ContactsRepository
from hometasks.contacts_api.core.depends import get_contacts_repository
from hometasks.contacts_api.core.responses import ResponseEntity, ResponseMeta

app = FastAPI()


@app.get("/status", description='test')
async def root():
    return JSONResponse({"status": "OK"})


@app.post("/contacts", description='create contact')
@handle_endpoint_errors
async def create_contact(
        contact: ContactBase,
        request: Request,
        repository: ContactsRepository = Depends(get_contacts_repository)
):
    contact = await repository.create_contact(contact)

    response = ResponseEntity(
        data=((contact_dict := contact.dict()), ),
        meta=ResponseMeta(
            fields=list(contact_dict.keys()),
            items_count=1
        )
    )
    response.set_self_link(request.url.path)
    return JSONResponse(
        jsonable_encoder(response), 201
    )


@app.get("/contacts", description='get contacts')
@handle_endpoint_errors
async def get_contacts(
        request: Request,
        repository: ContactsRepository = Depends(get_contacts_repository),
        order_by: Optional[ContactFields] = Query(ContactFields.name),
        order_direction: Optional[OrderDirection] = Query(OrderDirection.ASC),
        filters: BaseModel = Depends(create_model('Filters', **{field.value: (Optional[str], None) for field in ContactFields})),
        limit: int = Query(5),
        offset: int = Query(0),
):
    contacts = await repository.get_contacts(
        order_by, order_direction, {k: v for k, v in filters.dict().items() if v is not None}, offset, limit
    )

    response = ResponseEntity(
        data=(contact.dict() for contact in contacts),
        meta=ResponseMeta(
            fields=list(contacts[0].dict().keys()) if len(contacts) > 0 else None,
            items_count=len(contacts),
            offset=offset
        )
    )
    response.set_self_link(request.url.path)

    return JSONResponse(jsonable_encoder(response))


@app.put("/contacts/{uid}", description='update contact')
@handle_endpoint_errors
async def update_contact(
        uid: str,
        contact: ContactBase,
        request: Request,
        repository: ContactsRepository = Depends(get_contacts_repository),
):
    try:
        contact_to_update = (await repository.get_contacts(filters={'uid': uid}))[0]
    except IndexError:
        raise NotFoundException(f'Contact wit uid: "{uid}" not found')

    contact_to_update, updated_fields = await repository.update_contact(contact, contact_to_update)

    response = ResponseEntity(
        data=((updated_contact_dict := contact_to_update.dict()), ),
        meta=ResponseMeta(
            fields=list(updated_contact_dict.keys()),
            updated_fields=updated_fields,
            items_count=1
        )
    )
    response.set_self_link(request.url.path)

    return JSONResponse(jsonable_encoder(response))


@app.delete("/contacts/{uid}", description='delete contact')
@handle_endpoint_errors
async def delete_contact(
        uid: str,
        repository: ContactsRepository = Depends(get_contacts_repository),
):
    try:
        contact_to_delete = (await repository.get_contacts(filters={'uid': uid}))[0]
    except IndexError:
        raise NotFoundException(f'Contact wit uid: "{uid}" not found')

    await repository.delete_contact(contact_to_delete)

    return Response(status_code=204)


@app.on_event('startup')
async def startup():
    await init_db()
