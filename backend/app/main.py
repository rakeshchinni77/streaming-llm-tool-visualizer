import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

load_dotenv()

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

# Register routers
try:
	from app.api.health import router as health_router

	app.include_router(health_router)
except Exception:
	logger.exception("Failed to include routers")


@app.get("/", include_in_schema=False)
def root() -> dict:
	return {"status": "ok"}
