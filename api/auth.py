from functools import wraps
from typing import Any, Callable

from flask import current_app, request


def require_token(f: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(f)
    def decorated(*args: Any, **kwargs: Any) -> Any:
        api_token: str | None = current_app.config.get("API_TOKEN")
        if not api_token:
            return f(*args, **kwargs)

        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer ") or auth_header[7:] != api_token:
            return {"error": "Unauthorized"}, 401

        return f(*args, **kwargs)

    return decorated
