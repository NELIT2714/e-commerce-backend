from fastapi import Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class APIKeyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, api_key: str):
        super().__init__(app)
        self.api_key = api_key

    async def dispatch(self, request: Request, call_next):
        api_key = request.headers.get("X-API-Key")
        if not api_key == self.api_key:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"error": "Invalid API key"})
        return await call_next(request)
    