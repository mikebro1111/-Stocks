from pydantic import BaseModel, EmailStr
from typing import Optional
from bson import ObjectId


class PyObjectId(ObjectId):
    """
    Custom Pydantic validator for MongoDB ObjectId.
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class UserBase(BaseModel):
    """
    Base model for user data.
    """

    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """
    Model for creating a new user.
    Inherits from UserBase and adds a password field.
    """

    password: str


class UserDB(UserBase):
    """
    Model for user data stored in the database.
    Inherits from UserBase and adds an id and hashed_password field.
    """

    id: PyObjectId
    hashed_password: str

    class Config:
        """
        Configuration settings for UserDB model.
        """

        orm_mode = True
        json_encoders = {
            ObjectId: str
        }


class Token(BaseModel):
    """
    Model for authentication token.
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Model for token payload data.
    """

    username: Optional[str] = None
