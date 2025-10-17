from sqlmodel import SQLModel, Field
from datetime import datetime

class UploadedFile(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    filename: str
    filepath: str
    upload_time: datetime = Field(default_factory=datetime.utcnow)