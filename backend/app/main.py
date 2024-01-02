from fastapi import FastAPI, Request, status
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

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
async def validation_exception_handler(
    request: Request, exc: ValidationError
):
    return await request_validation_exception_handler(request, exc)

@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    if exc.orig.pgcode == "23505": # Unique violation
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "An error occurred, please try again."}
        )

    raise exc
