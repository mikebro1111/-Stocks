from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    """
    Defines the user model with optional email, full name, and disabled status.
    """
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
