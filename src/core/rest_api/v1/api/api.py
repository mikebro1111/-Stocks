from .endpoints import user, data
from fastapi import FastAPI, Depends
from src.core.rest_api.v1.api.auth import get_current_user
from src.core.rest_api.v1.api.models import User


app = FastAPI()

# Include routers for user and data modules.
# Each router is assigned a path prefix "/api/v1/" and corresponding tags for grouping.
app.include_router(user.router, prefix="/api/v1/", tags=["users"])
app.include_router(data.router, prefix="/api/v1/", tags=["data"])


@app.post("/create-user")
async def create_user(user: User):
    """
    Create a new user in the system.
    """
    return {"username": user.username, "email": user.email}


@app.get("/token")
async def login_for_access_token(form_data: Depends()):
    """
    Authenticate a user and return an access token.
    """
    return {"access_token": "your_token", "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Retrieve the currently logged-in user's data.
    """
    return current_user
