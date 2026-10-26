import logging
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .config import load_config
from .routes import feed as feed_routes

config = load_config()
logging.basicConfig(
    level=config.log_level,
    format='{"level":"%(levelname)s","logger":"%(name)s","msg":"%(message)s"}',
)
log = logging.getLogger("feed-api")

app = FastAPI(title="Feed Ranking Service", version="0.1.0")


@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
    request.state.request_id = request_id
    log.info("request_start id=%s %s %s", request_id, request.method, request.url.path)
    response = await call_next(request)
    response.headers["x-request-id"] = request_id
    return response


@app.exception_handler(Exception)
async def unhandled_error(request: Request, exc: Exception):
    rid = getattr(request.state, "request_id", "unknown")
    log.exception("unhandled error id=%s", rid)
    return JSONResponse(status_code=500, content={"error": "internal server error"})


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(feed_routes.router)
