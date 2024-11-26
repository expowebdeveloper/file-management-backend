import os
from sqlalchemy.orm import Session
from app.schema.models import Document
from app.database.connection import STORAGE_PATH
from datetime import datetime
from app.schema.schema import DocumentCreate, DocumentList, DocumentResponse


def get_all_documents(db: Session, search: str = None, sort_by: str = "created_at", desc: bool = False):
    query = db.query(Document)
    if search:
        query = query.filter(Document.name.contains(search))
    if desc:
        query = query.order_by(getattr(Document, sort_by).desc())
    else:
        query = query.order_by(getattr(Document, sort_by))
    documents = query.all()
    if not documents:
        return DocumentList(
            total=0,
            documents=[]  # Return an empty list for documents
        )
    return DocumentList(
        total=len(documents),
        documents=[DocumentResponse.model_validate(
            doc, from_attributes=True) for doc in documents]
    )


def get_document_by_id(db: Session, id: int):
    document = db.query(Document).filter(Document.id == id).first()
    if document:
        return DocumentResponse.model_validate(document, from_attributes=True)
    return None


def create_document(db: Session, doc: DocumentCreate):
    existing_document = db.query(Document).filter(
        Document.name == doc.name).first()
    if existing_document:
        raise ValueError("Document with this name already exists")

    filename = f"{STORAGE_PATH}/{doc.name}"
    with open(filename, "w") as file:
        file.write(doc.content)

    new_document = Document(
        name=doc.name, content=doc.content, size=len(doc.content))
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    return DocumentResponse.model_validate(new_document, from_attributes=True)


def delete_document(db: Session, id: int):
    document = db.query(Document).filter(Document.id == id).first()
    if document:
        filename = f"{STORAGE_PATH}/{document.name}"
        if os.path.exists(filename):
            os.remove(filename)
        db.delete(document)
        db.commit()
    return document
