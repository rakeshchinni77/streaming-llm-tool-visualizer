from fastapi import APIRouter

router = APIRouter()


@router.get("/health", status_code=200)
def health() -> dict:
    """Simple health endpoint returning service status."""
    return {"status": "healthy"}
