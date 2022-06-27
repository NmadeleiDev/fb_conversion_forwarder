from fastapi import FastAPI, status
from fastapi.logger import logger
import fastapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .static_server import add_static_handler

from ..model.server_exception import ServerException
from ..model.err_msg import ErrorMsgModel

from .routers import admin, forwarder, login

def get_app() -> FastAPI:
    app = FastAPI(
        title="Facebook conversions forwarder backend API docs",
        description='',
        version="0.0.1",
        contact={
            "name": "Gregory Potemkin",
            "email": "potemkin3940@gmail.com",
        },
        docs_url="/docs",
        root_path="/api/v1",
        openapi_url="/api/v1/openapi.json"
    )

    add_static_handler(app)

    app.include_router(router=admin.router)
    app.include_router(router=forwarder.router)
    app.include_router(router=login.router)

    origins = [
        "*",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(Exception)
    async def server_exception_handler(request, exc):
        if isinstance(exc, ServerException):
            return JSONResponse(content=ErrorMsgModel(msg=exc.message).dict(), status_code=exc.http_code)
        else:
            logger.error(f'unknown exc: {exc}')
            return JSONResponse(content=ErrorMsgModel().dict(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return app