from fastapi import FastAPI
from fastapi.exception_handlers import request_validation_exception_handler
from pydantic import ValidationError

from app.api.v1.api import api_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(api_router, prefix=settings.API_V1_STR)


# Exception handlers

@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return await request_validation_exception_handler(request, exc)
