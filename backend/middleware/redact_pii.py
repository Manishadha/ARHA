import re

from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware

_PAT = re.compile(r"([A-Za-z0-9._%+-]+)@([A-Za-z0-9.-]+\.[A-Za-z]{2,})")


def _redact(s: str) -> str:
    return _PAT.sub("[redacted_email]", s)


class RedactPIIMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            logger.error(_redact(str(exc)))
            raise
