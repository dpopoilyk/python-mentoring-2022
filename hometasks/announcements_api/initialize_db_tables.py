from hometasks.announcements_api.core.db import init_db
import asyncio


if __name__ == "__main__":
    asyncio.run(init_db())
