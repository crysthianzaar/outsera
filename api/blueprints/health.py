from flask import Blueprint

bp = Blueprint("health", __name__)


@bp.get("/ping")
def ping():
    return {"status": "pong"}


@bp.get("/health")
def health():
    return {"status": "ok"}
