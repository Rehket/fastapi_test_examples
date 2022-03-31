import jwt
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_403_FORBIDDEN
from .controller import User, TokenPayload
from databases import Database
from typing import Optional
from fastapi_testing import config
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi_testing.db.base import get_db
from . import crud


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{config.OPEN_API_PREFIX}/services/login/access-token"
)

ALGORITHM = "HS256"
password_reset_jwt_subject = "preset"
access_token_jwt_subject = "access"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "sub": access_token_jwt_subject})
    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=ALGORITHM)


def verify_password_reset_token(token) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
        assert decoded_token["sub"] == password_reset_jwt_subject
        return decoded_token["email"]
    except jwt.InvalidTokenError:
        return None


async def get_current_user(
    token: str = Security(reusable_oauth2),
    async_db: Database = Depends(get_db),
):
    """
    Get the current user based on the token provided.
    TODO: Find a way to extract out the database dependency
    """
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    user = await crud.get(async_db, user_id=token_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(current_user: User = Security(get_current_user)):
    if not crud.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(current_user: User = Security(get_current_user)):
    if not crud.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
