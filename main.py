from fastapi import FastAPI

from core.handlers.registry import register_exception_handlers
from core.lifespan import lifespan
from api.v1.router import router

app = FastAPI(lifespan=lifespan)

register_exception_handlers(app)

app.include_router(router)
