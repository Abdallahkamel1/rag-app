from fastapi import FastAPI
from routes import base,data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    app_settings = get_settings()
    app.mongodb_client = AsyncIOMotorClient(app_settings.mongodb_url)
    app.mongodb = app.mongodb_client[app_settings.mongodb_database]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(base.base_router)
app.include_router(data.data_router)