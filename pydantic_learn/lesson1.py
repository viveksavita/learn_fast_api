from datetime import datetime, timezone, UTC
from uuid import UUID, uuid4
from typing import Literal, Annotated
from functools import partial # allow us to pass arguments to default_factory functions
from pydantic import BaseModel, Field, EmailStr, HttpUrl, ValidationError, SecretStr, field_validator, model_validator, computed_field


class User(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    username:str
    verified_at:datetime | None = None
    email:EmailStr
    bio:str = ""
    is_active:bool = True
    first_name:str | None = None
    last_name:str | None = None
    followers_count:int = 0
    password:SecretStr | None = None

    @field_validator('username')
    @classmethod
    def validator(cls , v:str) -> str:
        if not v.replace("_","").isalnum():
            raise ValueError("username must be alphanumeric with underscores allowed")
        return v.lower()
    
    
   # Example of computed fields
    @computed_field
    @property
    def display_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    @computed_field
    @property
    def is_influencer(self) -> bool:
        return (self.followers_count or 0) > 1000






# Example with error

try:
    user1 = User(
        uid=1,
        username=None,
        Email ="dhaanush@gmail.com",)
except ValidationError as e:
    print(e.json())



# Example of nested models

class Comment(BaseModel):
    content:str
    author_email:EmailStr
    likes:int = 0

# Example with Field/annotation

class BlogPost(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    title: Annotated[str, Field(min_length=5, max_length=100)]
    content:str
    published_at:datetime = Field(default_factory= lambda : datetime.now(tz=UTC))
    created_at:datetime = Field(default_factory= partial(datetime.now, tz=UTC))
    author: User
    tags:list[str] = Field(default_factory=list)
    website:HttpUrl | None = None 
    status :Literal["draft", "published", "archived"] = "draft"
    age:Annotated[int, Field(gt=13, lt=100)] | None = None
    slug: Annotated[str, Field(pattern=r"^[a-z0-9-]+$")]
    comments:list[Comment] = Field(default_factory=list)




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



# example of blogpost distionary 

post_data = {
    "title": "Understanding Pydantic Models",
    "content": "Example of re-occurring calls",
    "slug": "understanding-pydantic",
    "author": {
        "username": "viveksavita",
        "email": "viveksavita@gmail.com",
        "age": 39,
        "password": "secret123",
    },
    "comments": [
        {
            "content": "Example of json seperated comments",
            "author_email": "test@example.com",
            "likes": 100,
        },
        {
            "content": "How to use Pydantic effectively in FastAPI",
            "author_email": "viveksavita@example.com",
            "likes": 200,
        },
    ],
}


post = BlogPost(**post_data)
print(post.model_dump_json(indent=2))