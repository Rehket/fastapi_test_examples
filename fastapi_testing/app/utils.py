from databases import Database
from fastapi_testing.services.users import crud, controller
from fastapi_testing import config


async def setup_db(db: Database):

    await db.execute("""
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name varchar(255) null,
        email varchar(255) not null unique,
        hashed_password varchar null,
        is_active bool null,
        is_superuser bool null
    );
    """)

    user = await crud.get_by_email(async_db=db, email=config.FIRST_SUPERUSER)
    if user is None:
        await crud.create(async_db=db, user_in=controller.UserCreate(
            email=config.FIRST_SUPERUSER,
            password=config.FIRST_SUPERUSER_PASSWORD,
            is_active=True,
            is_superuser=True
        ))
