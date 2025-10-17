from fastapi import APIRouter
from app.services import example_service

router = APIRouter(prefix="/api", tags=["basic"])

@router.get("/ping")
def ping():
    """Rota simples de teste."""
    return {"status": "ok", "message": "pong"}

@router.get("/process")
def process_image():
    """Simula um processamento de imagem."""
    result = example_service.fake_processing()
    return {"status": "success", "result": result}
