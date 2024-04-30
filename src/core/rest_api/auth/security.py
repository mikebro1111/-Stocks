from fastapi import HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from starlette import status
from src.core.rest_api.data.models import TokenData

# Configuration constants
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict):
    """
    Create a new access token with the provided data, including expiration.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    """
    Verify the authenticity of the provided JWT token and decode the user information.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data


def hash_password(password: str):
    """
    Hash a password using bcrypt, which automatically handles salting.
    """
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    """
    Verify if the plain password matches the hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)
