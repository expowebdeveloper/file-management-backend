from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class DocumentBase(BaseModel):
    name: str
    content: str

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: int
    created_at: datetime
    size: int

    class Config:
        orm_mode = True

class DocumentList(BaseModel):
    total: int
    documents: List[DocumentResponse]

class DocumentDeleteResponse(BaseModel):
    message: str

class DocumentError(BaseModel):
    detail: str
