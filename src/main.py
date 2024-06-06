from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .router import api_router

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
]

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="BanPay Take Home Assignment API",
    version="0.0.1",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    middleware=middleware,
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": str(exc)}),
    )