# app/routes/image_routes.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Body
from fastapi.responses import FileResponse
from sqlmodel import Session, select
from app.db.database import get_session
from app.models.file_model import UploadedFile
from datetime import datetime
import shutil, os, imghdr

router = APIRouter(prefix="/api/images", tags=["images"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# --- CREATE ---
@router.post("/")
def upload_image(file: UploadFile = File(...), db: Session = Depends(get_session)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Apenas arquivos de imagem são permitidos")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if imghdr.what(file_path) is None:
        os.remove(file_path)
        raise HTTPException(status_code=400, detail="Arquivo inválido: não é uma imagem")

    db_file = UploadedFile(filename=file.filename, filepath=file_path, upload_time=datetime.utcnow())
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return {"message": "Upload bem-sucedido", "file": db_file}


# --- READ (listagem) ---
@router.get("/")
def list_images(db: Session = Depends(get_session)):
    files = db.exec(select(UploadedFile)).all()
    return files


# --- READ (download) ---
@router.get("/{file_id}/download")
def download_image(file_id: int, db: Session = Depends(get_session)):
    db_file = db.get(UploadedFile, file_id)
    if not db_file:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    return FileResponse(path=db_file.filepath, filename=db_file.filename)


# --- UPDATE ---
@router.put("/rename/{file_id}")
def rename_image(
    file_id: int,
    new_name: str = Body(..., embed=True),
    db: Session = Depends(get_session)
):
    db_file = db.get(UploadedFile, file_id)
    if not db_file:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")

    old_path = os.path.abspath(db_file.filepath)
    file_ext = os.path.splitext(old_path)[1]
    new_filename = f"{new_name}{file_ext}"
    new_path = os.path.join(UPLOAD_DIR, new_filename)

    if not os.path.exists(old_path):
        raise HTTPException(status_code=404, detail=f"Arquivo físico não encontrado: {old_path}")

    if os.path.exists(new_path):
        raise HTTPException(status_code=400, detail="Já existe um arquivo com esse nome")

    try:
        os.rename(old_path, new_path)
    except OSError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao renomear: {e}")

    db_file.filename = new_filename
    db_file.filepath = new_path
    db.commit()
    db.refresh(db_file)

    return {"message": "Arquivo renomeado com sucesso", "file": db_file}


# --- DELETE ---
@router.delete("/{file_id}")
def delete_image(file_id: int, db: Session = Depends(get_session)):
    db_file = db.get(UploadedFile, file_id)
    if not db_file:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")

    if os.path.exists(db_file.filepath):
        os.remove(db_file.filepath)

    db.delete(db_file)
    db.commit()
    return {"message": "Arquivo removido com sucesso"}
