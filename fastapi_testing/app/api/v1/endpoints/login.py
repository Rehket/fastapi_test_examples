from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from fastapi_testing.services.users import crud as user_crud
from fastapi_testing.db.base import get_db
from fastapi_testing.services.users.security import get_current_user, create_access_token
from fastapi_testing.services.users.controller import Token, User, UserORM

from databases import Database
from fastapi_testing import config

router = APIRouter()


@router.post("/access-token", response_model=Token, tags=["login"])
async def login_access_token(
    async_db: Database = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await user_crud.authenticate(
        async_db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user_crud.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            data={"user_id": user.id}, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/test-token", tags=["login"], response_model=User)
async def test_token(current_user: UserORM = Depends(get_current_user)):
    """
    Test access token
    """
    return current_user
