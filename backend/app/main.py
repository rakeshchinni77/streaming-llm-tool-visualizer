import logging

from fastapi import FastAPI
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

# Register routers
app.include_router(health_router)
app.include_router(chat_router, prefix="/api/chat", tags=["Chat"])


@app.get("/", include_in_schema=False)
def root() -> dict:
    return {"status": "ok"}
