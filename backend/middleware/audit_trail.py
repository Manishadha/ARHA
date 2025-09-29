from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from loguru import logger
from backend.utils.logging import set_request_id


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        rid = set_request_id()
        logger.info(f"request_start {request.method} {request.url.path}")
        try:
            response: Response = await call_next(request)
            logger.info(
                f"request_end {request.method} {request.url.path} {response.status_code}"
            )
            return response
        except Exception as exc:
            logger.error(
                f"request_error {request.method} {request.url.path} {exc.__class__.__name__}"
            )
            raise
