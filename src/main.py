from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from src.models import Base
from src.routes import router
from src.schemas import ResponseStatus


@asynccontextmanager
async def lifespan(app: FastAPI):
    from src.db import engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(ResponseStatus(status=exc.args).model_dump(), status_code=400)


app.include_router(router)
