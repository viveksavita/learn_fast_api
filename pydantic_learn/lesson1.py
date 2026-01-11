from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, HttpUrl, ValidationError


class User(BaseModel):
    uid: int
    username:str
    verified_at:datetime | None = None
    Email:str
    bio:str = ""
    is_active:bool = True
    full_name:str | None = None

user = User(
    uid=1,
    username="dhaanush",
    Email ="dhaanush@gmail.com",)


# example to see the output of the class model

print(user.uid)
user.bio = "data scientist"

print(user.model_dump_json(indent=2))


# Example with error

try:
    user1 = User(
        uid=1,
        username=None,
        Email ="dhaanush@gmail.com",)
except ValidationError as e:
    print(e.json())
