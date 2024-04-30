from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import Optional
from pydantic import BaseModel
from src.core.rest_api.auth.security import SECRET_KEY, ALGORITHM
from src.core.rest_api.data.mongo_manager import get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    """
    Defines the user model with optional email, full name, and disabled status.
    """
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Retrieves the current user based on the provided token. Verifies the token's
    validity and decodes it to extract the username. If the token is invalid or the
    user does not exist, raises an HTTPException.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = get_user_by_username(username)
        if user is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return User(username=user["username"], email=user["email"], full_name=user["full_name"])
