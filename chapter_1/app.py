from fastapi import FastAPI
from pydantic_settings import BaseSettings
from enum import Enum

class Settings(BaseSettings):
    app_name: str = "My FastAPI App"
    app_version: str = "1.0.0"
    admin_email: str = "test@example.com"
    items_per_user: int = 50

settings = Settings()

# Example class for enumeration in path

class ModelName(str, Enum) :
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

@app.get("/info")
async def info():
    return {
        "app_name": settings.app_name,
        "app_version": settings.app_version,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }

@app.get("/custom/{your_name}")
async def custom(your_name: str):
    return {
        "Name:": your_name
    }

@app.get("/model/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    
    return {"model_name": model_name, "message": "Have some residuals"}