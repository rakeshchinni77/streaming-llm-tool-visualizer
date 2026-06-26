import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware

from app.config import ROOT_ENV_PATH, ENV_FILE_EXISTS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Streaming LLM Tool Visualizer API", version="1.0.0")

# CORS configuration
ALLOWED_ORIGINS = [
	"http://localhost:5173",
	"http://127.0.0.1:5173",
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=ALLOWED_ORIGINS,
	allow_credentials=True,
	allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
	allow_headers=["*"],
)

from app.api.health import router as health_router
from app.api.chat import router as chat_router
from app.api.summarize import router as summarize_router

# Register routers
app.include_router(health_router)
app.include_router(chat_router, prefix="/api/chat", tags=["Chat"])
app.include_router(summarize_router, prefix="/api/chat", tags=["Chat"])


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning("Validation failed for %s: %s", request.url, exc.errors())
    return JSONResponse(
        status_code=422,
        content={
            "message": "Invalid request body. Please check the JSON structure.",
            "detail": exc.errors(),
        },
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning("HTTP exception for %s: %s", request.url, exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc.detail) if exc.detail else "Request failed."},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unexpected error handling request %s", request.url)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error. Please try again later."},
    )


@app.get("/", include_in_schema=False)
def root() -> dict:
    return {"status": "ok"}
