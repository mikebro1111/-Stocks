from fastapi import APIRouter, HTTPException
from src.core.rest_api.auth.security import create_access_token
from src.core.rest_api.data.models import Token, UserCreate
from src.core.rest_api.data.mongo_manager import get_user_by_username, create_user
from slowapi.util import get_remote_address
from slowapi import Limiter


router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post("/users/", response_model=Token)
@limiter.limit("5/minute")
async def create_user_endpoint(user: UserCreate):
    """
    Create a new user endpoint.
    """
    if get_user_by_username(user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    user_id = create_user(user.dict())
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
