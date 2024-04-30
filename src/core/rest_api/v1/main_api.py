import uvicorn
from src.core.rest_api.v1.api.api import app

if __name__ == "__main__":
    """
    Entry point for running the FastAPI application.
    """
    uvicorn.run(app, host="0.0.0.0", port=8000)
