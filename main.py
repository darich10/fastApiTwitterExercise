# Python
from uuid import UUID
from datetime import date
from typing import Optional

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

# fastApi
from fastapi import FastAPI

app = FastAPI()

# Models
class UserBase(BaseModel):
    userID: UUID = Field(...)
    email: EmailStr = Field(...)

class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8
    )

class User(UserBase):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    birth_date: Optional[date] = Field(default=None)

class Tweet(BaseModel):
    pass


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
