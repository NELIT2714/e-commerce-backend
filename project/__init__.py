import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


from .logger import logger
from .database.mariadb import create_tables


@asynccontextmanager
async def lifespan(app_class: FastAPI):
    from .database.mariadb import models

    await create_tables()
    logger.info("Database initialized")
    yield


app = FastAPI(
    title="E-commerce API",
    debug=True if os.getenv("MODE") == "DEV" else False,
    docs_url="/",
    redoc_url="/redoc" if os.getenv("MODE") == "DEV" else None,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class APIKeyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, api_key: str):
        super().__init__(app)
        self.api_key = api_key

    async def dispatch(self, request: Request, call_next):
        api_key = request.headers.get("X-API-Key")
        if not api_key == self.api_key:
            return JSONResponse(status_code=401, content={"error": "Invalid API key"})
        return await call_next(request)

app.add_middleware(APIKeyMiddleware, api_key=os.getenv("API_KEY"))
    

router = APIRouter()
router_v1 = APIRouter(prefix="/v1")

from .routes import health, users, categories

router.include_router(router_v1)
app.include_router(router)

logger.info("API is up and running")
