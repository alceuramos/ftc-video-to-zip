from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCredentials(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int | None = None
    name: str
    email: EmailStr

    is_admin: bool
    is_reader: bool
    is_editor: bool

    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(extra="ignore", from_attributes=True)


class UserInput(User):
    password: str | None

    is_admin: bool | None = Field(default=False)
    is_reader: bool | None = Field(default=True)
    is_editor: bool | None = Field(default=False)


class UserUpdate(BaseModel):
    is_admin: bool | None = Field(default=None)
    is_reader: bool | None = Field(default=None)
    is_editor: bool | None = Field(default=None)
