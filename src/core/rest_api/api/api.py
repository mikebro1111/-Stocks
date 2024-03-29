from fastapi import FastAPI
from .endpoints import user, data

app = FastAPI()

# Include routers for user and data modules.
# Each router is assigned a path prefix "/api" and corresponding tags for grouping.
app.include_router(user.router, prefix="/api", tags=["users"])
app.include_router(data.router, prefix="/api", tags=["data"])
