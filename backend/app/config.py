import logging
import os
from pathlib import Path

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).resolve().parents[2]
ROOT_ENV_PATH = ROOT_DIR / ".env"
ENV_FILE_EXISTS = ROOT_ENV_PATH.exists()

if ENV_FILE_EXISTS:
    load_dotenv(ROOT_ENV_PATH, override=False)
else:
    load_dotenv(override=False)

logger.info("ROOT_ENV_PATH: %s", ROOT_ENV_PATH)
logger.info("ENV_FILE_EXISTS: %s", ENV_FILE_EXISTS)
logger.info(
    "LLM_API_KEY_LOADED: %s",
    bool(os.getenv("LLM_API_KEY") or os.getenv("GROQ_API_KEY")),
)
logger.info(
    "LLM_MODEL: %s",
    os.getenv("LLM_MODEL") or os.getenv("MODEL_NAME", "llama-3.3-70b-versatile"),
)
