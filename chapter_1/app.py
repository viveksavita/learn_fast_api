from fastapi import FastAPI
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My FastAPI App"
    app_version: str = "1.0.0"
    admin_email: str = "test@example.com"
    items_per_user: int = 50

settings = Settings()

app = FastAPI()

@app.get("/info")
async def info():
    return {
        "app_name": settings.app_name,
        "app_version": settings.app_version,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }