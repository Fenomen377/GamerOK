from datetime import datetime
from typing import Optional

from fastapi import HTTPException, Request, Depends
from jose import jwt, JWTError
from starlette import status

from config import settings
from exceptions import TokenAbsentException, IncorrectTokenFormatException, TokenExpiredException, \
    UserIsNotPresentException
from users.dao import UserDAO
from users.models import Users


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(request: Request) -> Optional[Users]:
    token = request.cookies.get("booking_access_token")
    if not token:
        return None  # Токена нет, пользователь не авторизован

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        expire = payload.get("exp")
        if not expire or int(expire) < datetime.utcnow().timestamp():
            return None  # Токен истек, пользователь не авторизован
        user_id = payload.get("sub")
        if not user_id:
            return None
        user = await UserDAO.find_one_or_none(id=int(user_id))
        return user
    except JWTError:
        return None
