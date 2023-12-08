from fastapi import FastAPI
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from app.api.v1.api import api_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS.ALLOW_ORIGINS,
    allow_credentials=settings.CORS.ALLOW_CREDENTIALS,
    allow_methods=settings.CORS.ALLOW_METHODS,
    allow_headers=settings.CORS.ALLOW_HEADERS
)

app.include_router(api_router, prefix=settings.API_V1_STR)


# Exception handlers

@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return await request_validation_exception_handler(request, exc)
