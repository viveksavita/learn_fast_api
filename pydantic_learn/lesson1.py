from datetime import datetime, timezone, UTC
from typing import Literal, Annotated
from functools import partial # allow us to pass arguments to default_factory functions
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


# Example with Field

class BlogPost(BaseModel):
    id:Annotated[int, Field(gt=0)] # of adding validation and metadata
    title: Annotated[str, Field(min_length=5, max_length=100)]
    content:str
    published_at:datetime = Field(default_factory= lambda : datetime.now(tz=UTC))
    created_at:datetime = Field(default_factory= partial(datetime.now, tz=UTC))
    author_email:EmailStr
    tags:list[str] = Field(default_factory=list)
    website:HttpUrl | None = None 
    status :Literal["draft", "published", "archived"] = "draft"
    age:Annotated[int, Field(gt=13, lt=100)] | None = None



post1 = BlogPost(id=1,title="My First Post",
                     content="This is the content of my first post.", author_email="dhaanush@gmail.com")
    
print(post1.model_dump_json(indent=2))