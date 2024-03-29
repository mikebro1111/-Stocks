from fastapi import APIRouter, Depends, HTTPException
from src.core.rest_api.auth.ouath2 import get_current_user
from src.core.rest_api.data.models import UserDB
from src.core.rest_api.data.mongo_manager import get_user_data

router = APIRouter()


@router.get("/data/")
async def read_data(current_user: UserDB = Depends(get_current_user)):
    """
    Retrieves data associated with the current user.
    """
    data = get_user_data(current_user.username)
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    return {"data": data}
