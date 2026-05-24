from __future__ import annotations

from fastapi import Request
from itsdangerous import BadSignature, URLSafeSerializer
from passlib.context import CryptContext
from starlette.responses import Response

from packages.core.config import Settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, password_hash: str) -> bool:
    try:
        return pwd_context.verify(plain_password, password_hash)
    except Exception:
        return False


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def _serializer(settings: Settings) -> URLSafeSerializer:
    return URLSafeSerializer(settings.app_session_secret, salt="trading-system-session")


def create_session_cookie_value(settings: Settings) -> str:
    return _serializer(settings).dumps({"version": 1, "authenticated": True})


def is_authenticated(request: Request, settings: Settings) -> bool:
    cookie = request.cookies.get(settings.session_cookie_name)
    if not cookie:
        return False
    try:
        payload = _serializer(settings).loads(cookie)
    except BadSignature:
        return False
    return bool(payload.get("authenticated"))


def clear_session_cookie(response: Response, settings: Settings) -> None:
    response.delete_cookie(settings.session_cookie_name)
