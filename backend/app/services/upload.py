import os
from fastapi import UploadFile
from sqlmodel import Session
from app.models.file_model import UploadedFile

UPLOAD_DIR = "uploads"

def save_uploaded_file(file: UploadFile, session: Session) -> UploadedFile:
    """Salva o arquivo e cria um registro no banco."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    record = UploadedFile(filename=file.filename, filepath=file_path)
    session.add(record)
    session.commit()
    session.refresh(record)

    return record
