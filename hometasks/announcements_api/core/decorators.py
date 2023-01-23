import traceback
from functools import wraps

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from asyncpg import PostgresError
from sqlalchemy.exc import SQLAlchemyError

from hometasks.announcements_api.core.exceptions import (
    DatabaseException,
    NotFoundException,
)
from hometasks.announcements_api.core.responses import ErrorResponse
from hometasks.announcements_api.core.utils import get_logger

logger = get_logger(__name__)


def handle_database_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except (PostgresError, SQLAlchemyError) as err:
            logger.debug(traceback.format_exc())
            raise DatabaseException(f"Database exception: {str(err)}")

    return wrapper


def handle_endpoint_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except DatabaseException as err:
            logger.error(err)
            return JSONResponse(
                jsonable_encoder(
                    ErrorResponse(
                        title="Service exception.",
                        detail="There is error with Postgesql database.",
                    )
                ),
                400,
            )
        except NotFoundException as err:
            logger.error(err)
            return JSONResponse(
                jsonable_encoder(
                    ErrorResponse(title="Item not found.", detail=str(err))
                ),
                404,
            )

    return wrapper
