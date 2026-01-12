from datetime import datetime, timezone, UTC
from uuid import UUID, uuid4
from typing import Literal, Annotated
from functools import partial # allow us to pass arguments to default_factory functions
from pydantic import BaseModel, Field, EmailStr, HttpUrl, ValidationError, SecretStr, field_validator, model_validator


class User(BaseModel):
    uid: int
    username:str
    verified_at:datetime | None = None
    Email:str
    bio:str = ""
    is_active:bool = True
    full_name:str | None = None

    @field_validator('username')
    @classmethod
    def validator(cls , v:str) -> str:
        if not v.replace("_","").isalnum():
            raise ValueError("username must be alphanumeric with underscores allowed")
        return v.lower()


user = User(
    uid=1,
    username="dhaanush_VIEK_99",
    Email ="dhaanush@gmail.com",)


# example to see the output of the class model

print(user.uid)
print(user.username)
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


# Example with Field/annotation

class BlogPost(BaseModel):
    id:Annotated[int, Field(gt=0)] # of adding validation and metadata
    uid: UUID = Field(default_factory=uuid4)
    title: Annotated[str, Field(min_length=5, max_length=100)]
    content:str
    published_at:datetime = Field(default_factory= lambda : datetime.now(tz=UTC))
    created_at:datetime = Field(default_factory= partial(datetime.now, tz=UTC))
    author_email:EmailStr
    tags:list[str] = Field(default_factory=list)
    website:HttpUrl | None = None 
    status :Literal["draft", "published", "archived"] = "draft"
    age:Annotated[int, Field(gt=13, lt=100)] | None = None
    slug: Annotated[str, Field(pattern=r"^[a-z0-9-]+$")]
    password:SecretStr


try:
    post1 = BlogPost(id=1,title="test_title",
                        content="This is the content of my first post.", 
                        author_email="dhaanush@gmail.com"
                        ,slug="my-first-post"
                        , password="supersecret"
                        )
except ValidationError as e:
    print(e.json())

    
print(post1.model_dump_json(indent=2))
print( post1.password.get_secret_value() )  # Accessing the secret value



#Example of model validator

class UserRegistration(BaseModel):
    username:EmailStr
    password:str
    confirm_password:str

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
    

try:
    user_reg = UserRegistration(
        username="dhaanush@gmail.com",
        password="supersecret",
        confirm_password="supers1ecret"
    )
except ValidationError as e:
    print(e.json())