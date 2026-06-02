from fastapi import APIRouter, Depends
import os
from helpers.config import get_settings 

base_router = APIRouter()

@base_router.get("/welcome")

async def welcome(app_settings = Depends(get_settings)):
    #app_settings = get_settings()

    return {
        "app_name" : app_settings.app_name,
        "app_version" : app_settings.app_version
    }
